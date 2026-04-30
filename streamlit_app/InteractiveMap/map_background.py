import pandas as pd
import geopandas as gpd
import holoviews as hv
import geoviews as gv
import numpy as np
import panel as pn
import tempfile
from shapely import wkt


from bokeh.models import HoverTool, Span, CustomJS
hv.extension("bokeh")
gv.extension("bokeh")
pn.extension()

def prepare_map_data(fetch_response):
    data = fetch_response.json()[0]

    df = pd.DataFrame(data['county_data'])
    df_county = pd.json_normalize(df["county"]).drop(columns=["id"])
    df = pd.concat([df.drop(columns=["county"]), df_county],axis=1).drop(columns=["id"])
    df["geometry"] = df["geometry"].apply(wkt.loads)

    df = gpd.GeoDataFrame(df, geometry="geometry",crs="EPSG:4326")

    edges={}
    edges["vmin"] = df["infections"].min()
    edges["vmax"] = df["infections"].max()

    return df, edges

def make_colorbar(shared, vmin, vmax):
    x = np.linspace(vmin, vmax, 256)
    y = [0, 1]
    z = np.vstack([x, x])

    def colorbar_hook(plot, element):
        fig = plot.state

        span = Span(
            location=vmin,
            dimension="height",
            line_color="black",
            line_width=2,
            visible=False,
        )

        fig.add_layout(span)
        shared["span"] = span

    return hv.Image((x, y, z)).opts(
        width=300,
        height=30,
        cmap="RdPu",
        clim=(vmin, vmax),
        colorbar=False,
        xticks=[(vmin, f"{vmin:.2f}"), (vmax, f"{vmax:.2f}")],
        toolbar=None,
        yaxis=None,
        show_frame=False,
        hooks=[colorbar_hook],
    )

def load_polygon(date, precomputed, edges):
    shared = {}

    vmin = edges["vmin"]
    vmax = edges["vmax"]

    hover = HoverTool(
        tooltips=[
            ("County", "@name"),
            ("Weekly new cases per 100 000 people", "@infections{0.00}"),
        ]
    )

    colorbar = make_colorbar(shared, vmin, vmax)

    def map_hook(plot, element):
        fig = plot.state

        renderer = None
        for r in fig.renderers:
            if hasattr(r, "data_source"):
                renderer = r
                break

        if renderer is None or "span" not in shared:
            return

        source = renderer.data_source
        span = shared["span"]

        hover_tool = None
        for t in fig.tools:
            if isinstance(t, HoverTool):
                hover_tool = t
                break

        if hover_tool is None:
            return

        hover_tool.callback = CustomJS(
            args=dict(source=source, span=span),
            code="""
                const inds = cb_data.index.indices;

                if (inds.length > 0) {
                    const i = inds[0];
                    const vals = source.data["infections"];
                    span.location = vals[i];
                    span.visible = true;
                } else {
                    span.visible = false;
                }
            """,
        )

    def transparent_hook(plot, element):
        fig = plot.state
        fig.background_fill_color = None
        fig.border_fill_color = None
        fig.outline_line_color = None

    poly = gv.Polygons(
        precomputed,
        vdims=["name", "infections"],
    ).opts(
        width=700,
        height=500,
        color="infections",
        cmap="RdPu",
        clim=(vmin, vmax),
        colorbar=False,
        line_color="white",

        bgcolor=None,
        border=0,
        margin=0,
        padding=0,
        show_frame=False,
        xaxis=None,
        yaxis=None,
        toolbar=None,

        line_width=1,
        fill_alpha=0.6,
        tools=[hover],
        hover_line_color="black",
        hover_fill_alpha=0.8,
        title="",
        hooks=[map_hook, transparent_hook],
    )

    colorbar_row = pn.Row(
        pn.Spacer(width=130),
        colorbar,
        pn.Spacer(),
        width=700
    )

    return pn.Column(colorbar_row, poly, styles={"background": "transparent"})

def panel_to_html(panel_object):
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        panel_object.save(tmp.name, resources="cdn", embed=True)

        with open(tmp.name, "r", encoding="utf-8") as f:
            html = f.read()

    return html