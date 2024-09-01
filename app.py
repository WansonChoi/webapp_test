import os, sys, re
# import numpy as np
import pandas as pd
from functools import reduce


# from umap import UMAP
# import umap.umap_ as UMAP

import plotly.express as px
# from sklearn.datasets import load_digits

## Dash 관련
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, State
from dash import jupyter_dash
from dash import dash_table
# from dash import html, dcc, Input, Output, State
# import dash_table

import matplotlib.pyplot as plt

### app.py로 만들면서 load해줘야하는 부분들.
from src.plotly_UMAP_main import plotly_UMAP_main
from src.plotly_UMAP_rg import plotly_UMAP_rg



# Initialize the Dash app with the Litera theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA], suppress_callback_exceptions=True)




### 귀찮아서 그냥 global로 load해놓고 쓸 data들

## UKBB
df_UMAP_UKBB = pd.read_csv("data/UKBB.UMAP.T715.txt", sep='\t', header=0, index_col=0)
df_cmap_UKBB = pd.read_csv("data/UKBB.cmap.T715.txt", sep='\t', header=0, dtype=str)
df_rg_UKBB = pd.read_csv(
    "data/UKBB.T715.ctldsc_icor.gcor.gzip", sep='\t', header=0, compression='gzip',
    usecols=["id_phe1", "id_phe2", "phe1_name", "phe2_name", "gcor", "gcor_SE", "zscore", "P"]
)
# df_ToPlot_UKBB = pd.read_excel(
#     "data/SupplementaryTable1.xlsx", header=0, dtype={"Phenocode_nealelab": str}
# )
df_ToPlot_UKBB = pd.read_csv(
    "data/SupplementaryTable1.gzip", sep='\t', header=0, dtype={"Phenocode_nealelab": str},
    compression='gzip'
)



print(df_UMAP_UKBB)
print(df_cmap_UKBB)
print(df_rg_UKBB)
print(df_ToPlot_UKBB)



## BBJ
df_UMAP_BBJ = pd.read_csv("data/BBJ.UMAP.T220.txt", sep='\t', header=0, index_col=0)
df_cmap_BBJ = pd.read_csv("data/BBJ.cmap.T220.txt", sep='\t', header=0, dtype=str)
df_rg_BBJ = pd.read_csv(
    "data/BBJ.icor.ctldsc.T220.r24310.gcor.FIXED.20240314.gzip", sep='\t', header=0, compression='gzip',
    usecols=["phe1_name", "phe2_name", "gcor", "gcor_SE", "zscore", "P"]
)

# df_ToPlot_BBJ = pd.read_excel("data/SupplementaryTable2.xlsx", header=0)
df_ToPlot_BBJ = pd.read_csv("data/SupplementaryTable2.gzip", sep='\t', header=0, compression='gzip',)


print(df_UMAP_BBJ)
print(df_cmap_BBJ)
print(df_rg_BBJ)
print(df_ToPlot_BBJ)


### plotly UMAP 만들고 시작.

fig_UMAP_UKBB = plotly_UMAP_main(
    df_ToPlot_UKBB, "UKBB", df_UMAP_UKBB, df_cmap_UKBB, 
    _start_UMAP_xrange=(-45, 60), _start_UMAP_yrange=(-40, 50))

fig_UMAP_BBJ = plotly_UMAP_main(
    df_ToPlot_BBJ, "BBJ", df_UMAP_BBJ, df_cmap_BBJ,
    _start_UMAP_xrange=(-20, 30), _start_UMAP_yrange=(-20, 30))





# Define the main navigation bar
def create_navbar(active_path):
    def get_nav_item(name, path):
        return dbc.NavItem(
            dbc.NavLink(
                name, href=path, className="nav-link", active="exact" if active_path == path else ""
            )
        )

    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("Hanlab", href="/"),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Nav(
                                    [
                                        get_nav_item("Home", "/"),
                                        get_nav_item("UKBB", "/ukbb"),
                                        get_nav_item("BBJ", "/bbj"),
                                        get_nav_item("for Review (temp)", "/review"),
                                    ],
                                    className="ml-auto", navbar=True
                                ),
                            ),
                            dbc.Col(
                                dbc.Nav(
                                    [get_nav_item("About", "/about")],
                                    className="ms-auto", navbar=True
                                ),
                                width="auto",
                            ),
                        ],
                        align="center",
                        className="w-100",
                    ),
                    id="navbar-collapse", navbar=True
                ),
            ],
            fluid=True,
        ),
        color="primary",
        dark=True,
        fixed="top",
    )





def create_link_page_Review():
    sidebar = html.Div(
        [
            html.H2("Contents", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Community detection result on UMAP (UKBB)", href="#community_ukbb", className="nav-link"),
                    dbc.NavLink("Community detection result on UMAP (BBJ)", href="#community_bbj", className="nav-link"),
                    dbc.NavLink("Estimated r<sub>g</sub> on the UMAP (UKBB)", href="#estimated_rg_ukbb", className="nav-link"),
                    dbc.NavLink("Estimated r<sub>g</sub> on the UMAP (BBJ)", href="#estimated_rg_bbj", className="nav-link"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style={"position": "fixed", "top": "70px", "left": "0", "bottom": "0", "width": "250px", "padding": "20px", "background-color": "#f8f9fa"},
    )

    content = html.Div(
        [
            html.H2("Community detection result on UMAP (UKBB)", id="community_ukbb"),
            html.P("This is the community detection result on UMAP content for UKBB.", style={'font-family': 'Arial'}),
            html.H2("Community detection result on UMAP (BBJ)", id="community_bbj"),
            html.P("This is the community detection result on UMAP content for BBJ.", style={'font-family': 'Arial'}),
            html.H2("Estimated r<sub>g</sub> on the UMAP (UKBB)", id="estimated_rg_ukbb"),
            html.P("This is the estimated r<sub>g</sub> on the UMAP content for UKBB.", style={'font-family': 'Arial'}),
            html.H2("Estimated r<sub>g</sub> on the UMAP (BBJ)", id="estimated_rg_bbj"),
            html.P("This is the estimated r<sub>g</sub> on the UMAP content for BBJ.", style={'font-family': 'Arial'}),
        ],
        style={"margin-left": "270px", "padding": "20px"},
    )

    return sidebar, content





def create_link_page_Home():
    sidebar = None
    content = html.Div(
        [
            html.H2("Welcome to Hanlab"),
            html.P("This is the home page content.", style={'font-family': 'Arial'}),
        ],
        style={"padding": "20px"},
    )

    return sidebar, content





def create_link_page_About():
    sidebar = None
    content = html.Div(
        [
            html.H2("About"),
            html.P("This is the about page content.", style={'font-family': 'Arial'}),
        ],
        style={"padding": "20px"},
    )

    return sidebar, content




def create_link_page_BBJ(_fig_UMAP_BBJ, _df_ToPlot_BBJ: pd.DataFrame):
    
    ##### Sidebar
    sidebar = html.Div(
        [
            html.H2("Contents", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Community detection result", href="#community_BBJ", className="nav-link", external_link=True),
                    dbc.NavLink("UMAP", href="#umap_BBJ", className="nav-link", external_link=True),
                    dbc.NavLink([html.Span(["Estimated r", html.Sub("g"), " on the UMAP"])], href="#estimated_rg_BBJ", className="nav-link", external_link=True),                    
                    dbc.NavLink("tSNE", href="#tsne_BBJ", className="nav-link", external_link=True),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style={"position": "fixed", "top": "70px", "left": "0", "bottom": "0", "width": "250px", "padding": "20px", "background-color": "#f8f9fa"},
    )

    
    
    ##### Contents
    l_contents = []

    ### [1] Community Detection result.
    content_CM = [
        html.H2("Community detection result", id="community_BBJ"),
        html.P("This is the community detection result content for BBJ.", style={'font-family': 'Arial'}),
        # html.Div(style={"height": "600px"}),  # 여백 추가
    ]

    ### [2] UMAP
    content_UMAP = [
        html.H2("UMAP", id="umap_BBJ"),
        html.P("This is the UMAP content for BBJ.", style={'font-family': 'Arial'}),
        html.Div([
            html.Div(dcc.Graph(id='UMAP_BBJ', figure=_fig_UMAP_BBJ), style={'display': 'flex', 'justifyContent': 'center'})
        ], style={'width': '100%'}),
        # html.Div(style={"height": "600px"}),  # 여백 추가
    ]
    
    ### [3] UMAP_rg
    content_UMAP_rg = [
        html.Div(
            children=[
                html.H2(id="estimated_rg_BBJ", children=["Estimated ", html.I("r"), html.Sub("g"), " on the UMAP"]),
                html.P(children=["This is the estimated ", html.I("r"), html.Sub("g"), " on the UMAP content for BBJ."], style={'font-family': 'Arial'}),
            ]
        ),        
        dash_table.DataTable(
            id='table_BBJ',
            columns=[{"name": i, "id": i} for i in _df_ToPlot_BBJ.columns],
            data=_df_ToPlot_BBJ.astype(str).to_dict('records'),
            style_table={'overflowY': 'auto', 'maxHeight': '400px'},  # Scroll 기능 추가
            style_cell={'font-family': 'Arial'},
            filter_action='native',  # 필터링 기능 추가
            sort_action='native',  # 정렬 기능 추가
            page_action='none',  # 페이지 기능 비활성화
        ),    
        html.Div(id='clicked-cell_BBJ', style={'marginTop': '20px'}),  # 클릭된 셀 값을 표시할 Div 추가
        html.Div(id='UMAP_rg_div_BBJ'),  # UMAP을 표시할 Div 추가
        # html.Div(style={"height": "600px"}),  # 여백 추가
    ]    

    ### [4] tSNE
    content_tSNE = [
        html.H2("tSNE", id="tsne_BBJ"),
        html.P("This is the tSNE content for BBJ.", style={'font-family': 'Arial'}),
        # html.Div(style={"height": "600px"}),  # 여백 추가
    ]

    
    ##### Wrap-up
    
    l_contents = [content_CM, content_UMAP, content_UMAP_rg, content_tSNE]

    def extend_contents(x: list, y: list) -> list:
        x.extend(y)
        return x
    
    l_contents = reduce(lambda x, y: extend_contents(x, y), l_contents)
    
    content = html.Div(
        l_contents,
        style={"margin-left": "270px", "padding": "20px"},
    )
    
    return sidebar, content





def create_link_page_UKBB(_fig_UMAP_UKBB, _df_ToPlot_UKBB: pd.DataFrame):
    
    ##### Sidebar
    sidebar = html.Div(
        [
            html.H2("Contents", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Community detection result", href="#community_UKBB", className="nav-link", external_link=True),
                    dbc.NavLink("UMAP", href="#umap_UKBB", className="nav-link", external_link=True),
                    dbc.NavLink([html.Span(["Estimated r", html.Sub("g"), " on the UMAP"])], href="#estimated_rg_UKBB", className="nav-link", external_link=True),                    
                    dbc.NavLink("tSNE", href="#tsne_UKBB", className="nav-link", external_link=True),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style={"position": "fixed", "top": "70px", "left": "0", "bottom": "0", "width": "250px", "padding": "20px", "background-color": "#f8f9fa"},
    )

    
    
    ##### Contents
    l_contents = []

    ### [1] Community Detection result.
    content_CM = [
        html.H2("Community detection result", id="community_UKBB"),
        html.P("This is the community detection result content for UKBB.", style={'font-family': 'Arial'}),
        # html.Div(style={"height": "600px"}),  # 여백 추가
    ]

    ### [2] UMAP
    content_UMAP = [
        html.H2("UMAP", id="umap_UKBB"),
        html.P("This is the UMAP content for UKBB.", style={'font-family': 'Arial'}),
        html.Div([
            html.Div(dcc.Graph(id='UMAP_UKBB', figure=_fig_UMAP_UKBB), style={'display': 'flex', 'justifyContent': 'center'})
        ], style={'width': '100%'}),
        # html.Div(style={"height": "600px"}),  # 여백 추가
    ]

    ### [3] UMAP_rg
    content_UMAP_rg = [
        html.Div(
            children=[
                html.H2(id="estimated_rg_UKBB", children=["Estimated ", html.I("r"), html.Sub("g"), " on the UMAP"]),
                html.P(children=["This is the estimated ", html.I("r"), html.Sub("g"), " on the UMAP content for UKBB."], style={'font-family': 'Arial'}),
            ]
        ),        
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in _df_ToPlot_UKBB.columns],
            data=_df_ToPlot_UKBB.astype(str).to_dict('records'),
            style_table={'overflowY': 'auto', 'maxHeight': '400px'},  # Scroll 기능 추가
            style_cell={'font-family': 'Arial'},
            filter_action='native',  # 필터링 기능 추가
            sort_action='native',  # 정렬 기능 추가
            page_action='none',  # 페이지 기능 비활성화
        ),    
        html.Div(id='clicked-cell', style={'marginTop': '20px'}),  # 클릭된 셀 값을 표시할 Div 추가
        html.Div(id='UMAP_rg_div'),  # UMAP을 표시할 Div 추가
        # html.Div(style={"height": "600px"}),  # 여백 추가
    ]    

    ### [4] tSNE
    content_tSNE = [
        html.H2("tSNE", id="tsne_UKBB"),
        html.P("This is the tSNE content for UKBB.", style={'font-family': 'Arial'}),
        # html.Div(style={"height": "600px"}),  # 여백 추가
    ]

    
    ##### Wrap-up
    
    l_contents = [content_CM, content_UMAP, content_UMAP_rg, content_tSNE]

    def extend_contents(x: list, y: list) -> list:
        x.extend(y)
        return x
    
    l_contents = reduce(lambda x, y: extend_contents(x, y), l_contents)
    
    content = html.Div(
        l_contents,
        style={"margin-left": "270px", "padding": "20px"},
    )
    
    return sidebar, content



# 클릭된 셀의 값을 가져와서 UMAP을 업데이트하는 콜백 함수
@app.callback(
    Output('UMAP_rg_div', 'children'),
    Output('clicked-cell', 'children'),
    [Input('table', 'active_cell')],
    [State('table', 'derived_virtual_data')]  # 필터링 및 정렬이 적용된 데이터를 가져옴
)
def update_umap(active_cell, derived_virtual_data):
    if active_cell:
        row = active_cell['row']
        target_trait = derived_virtual_data[row]["Phenocode_nealelab"]
        description = derived_virtual_data[row]["Description"]

        # 화면에 표시할 메시지
        clicked_cell_message = html.Div([
            html.P(f"Clicked trait: {target_trait}", style={'font-family': 'Arial'}),
            html.P(f"Clicked trait description: {description}", style={'font-family': 'Arial'})
        ])

        # 새로운 UMAP을 생성
        fig_UMAP_rg_UKBB, _ = plotly_UMAP_rg(df_UMAP_UKBB, df_rg_UKBB, target_trait, df_ToPlot_UKBB, "UKBB",
                                             _start_UMAP_xrange=(-45, 60), _start_UMAP_yrange=(-40, 50))
        return dcc.Graph(id='UMAP_rg_UKBB', figure=fig_UMAP_rg_UKBB), clicked_cell_message

    # 클릭되지 않은 초기 상태 메시지
    return dash.no_update, html.Div([
        html.P("Clicked trait: Not yet", style={'font-family': 'Arial'}),
        html.P("Clicked trait description: Not yet", style={'font-family': 'Arial'})
    ])



# 클릭된 셀의 값을 가져와서 UMAP을 업데이트하는 콜백 함수
@app.callback(
    Output('UMAP_rg_div_BBJ', 'children'),
    Output('clicked-cell_BBJ', 'children'),
    [Input('table_BBJ', 'active_cell')],
    [State('table_BBJ', 'derived_virtual_data')]  # 필터링 및 정렬이 적용된 데이터를 가져옴
)
def update_umap_BBJ(active_cell, derived_virtual_data):
    
    if active_cell:
                
        row = active_cell['row']
        target_trait = derived_virtual_data[row]["phe_name_dir (BBJ)"]
        description = derived_virtual_data[row]["phenostring (BBJ)"]

        # 화면에 표시할 메시지
        clicked_cell_message = html.Div([
            html.P(f"Clicked trait: {target_trait}", style={'font-family': 'Arial'}),
            html.P(f"Clicked trait description: {description}", style={'font-family': 'Arial'})
        ])

        # 새로운 UMAP을 생성
        fig_UMAP_rg_BBJ, _ = plotly_UMAP_rg(df_UMAP_BBJ, df_rg_BBJ, target_trait, df_ToPlot_BBJ, "BBJ",
                                             _start_UMAP_xrange=(-20, 30), _start_UMAP_yrange=(-20, 30))
        return dcc.Graph(id='UMAP_rg_BBJ', figure=fig_UMAP_rg_BBJ), clicked_cell_message

    # 클릭되지 않은 초기 상태 메시지
    return dash.no_update, html.Div([
        html.P("Clicked trait: Not yet", style={'font-family': 'Arial'}),
        html.P("Clicked trait description: Not yet", style={'font-family': 'Arial'})
    ])




# 대시보드 레이아웃 설정
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # URL 추적용 Location 컴포넌트 추가
    html.Div(id='navbar-container'),
    html.Div(id='sidebar-container'),
    html.Div(id='page-content', className='p-4', style={'marginTop': '70px'}),
    html.Div(id='dummy-output')  # JavaScript를 위한 dummy-output 추가
])

# 콜백 함수 설정
@app.callback(
    [Output('navbar-container', 'children'),
     Output('sidebar-container', 'children'),
     Output('page-content', 'children')],
    [Input('url', 'pathname')]
)
def display_page(pathname):
    navbar = create_navbar(pathname)
    sidebar = None
    content = None

    if pathname == '/ukbb':
        sidebar, content = create_link_page_UKBB(fig_UMAP_UKBB, df_ToPlot_UKBB)
    elif pathname == '/bbj':
        sidebar, content = create_link_page_BBJ(fig_UMAP_BBJ, df_ToPlot_BBJ)
    elif pathname == '/review':
        sidebar, content = create_link_page_Review()
    elif pathname == '/about':
        sidebar, content = create_link_page_About()
    else:
        sidebar, content = create_link_page_Home()

    return navbar, sidebar, content

app.clientside_callback(
    """
    function(href) {
        if (href) {
            const id = href.split("#")[1];
            if (id) {
                const element = document.getElementById(id);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                    const yOffset = -70;  // 여기서 오프셋 값을 조정하세요 (Navbar의 높이에 맞게 조정)
                    const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
                    window.scrollTo({ top: y, behavior: 'smooth' });
                }
            }
        }
    }
    """,
    Output('dummy-output', 'children'),
    [Input('url', 'href')]
)

# 대시보드 서버 실행
if __name__ == '__main__':
    app.run_server(debug=False, port=8000)