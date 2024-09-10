import os, sys, re
import pandas as pd
from functools import reduce

import plotly.express as px

## Dash 관련
import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Output, Input, State
from dash import jupyter_dash
from dash import dash_table
# from dash import html, dcc, Input, Output, State
# import dash_table

# import matplotlib.pyplot as plt

### app.py로 만들면서 load해줘야하는 부분들.
from src.plotly_UMAP_main import plotly_UMAP_main
from src.plotly_UMAP_rg import plotly_UMAP_rg



##### [0] Global Variables #####

####### [0-1] Initialize the Dash app with the Litera theme #####
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA], suppress_callback_exceptions=True)



####### [0-2] DataFrames and UMAP figures #####

"""
- Global로 빨리빨리 가져다 쓰는게 생각보다 나은 선택인듯 함.
- Callback function을 call할때 데이터프레임을 argument로 던지는게 생각보다 복잡함.
- 어차피 webapp의 규모도 작으니 그냥 global variable로 load해서 쓰는게 생각보다 효과적일듯함.

"""

## UKBB
df_UMAP_UKBB = pd.read_csv("/home/wschoi/webapp_test/data/UKBB.UMAP.T715.txt", sep='\t', header=0, index_col=0)
df_cmap_UKBB = pd.read_csv("/home/wschoi/webapp_test/data/UKBB.cmap.T715.txt", sep='\t', header=0, dtype=str)
df_rg_UKBB = pd.read_csv(
    "/home/wschoi/webapp_test/data/UKBB.T715.ctldsc_icor.gcor.gzip", sep='\t', header=0, compression='gzip',
    usecols=["id_phe1", "id_phe2", "phe1_name", "phe2_name", "gcor", "gcor_SE", "zscore", "P"]
)
# df_ToPlot_UKBB = pd.read_excel(
#     "data/SupplementaryTable1.xlsx", header=0, dtype={"Phenocode_nealelab": str}
# )
df_ToPlot_UKBB = pd.read_csv(
    "/home/wschoi/webapp_test/data/SupplementaryTable1.gzip", sep='\t', header=0, dtype={"Phenocode_nealelab": str},
    compression='gzip'
)



print(df_UMAP_UKBB)
print(df_cmap_UKBB)
print(df_rg_UKBB)
print(df_ToPlot_UKBB)



## BBJ
df_UMAP_BBJ = pd.read_csv("/home/wschoi/webapp_test/data/BBJ.UMAP.T220.txt", sep='\t', header=0, index_col=0)
df_cmap_BBJ = pd.read_csv("/home/wschoi/webapp_test/data/BBJ.cmap.T220.txt", sep='\t', header=0, dtype=str)
df_rg_BBJ = pd.read_csv(
    "/home/wschoi/webapp_test/data/BBJ.icor.ctldsc.T220.r24310.gcor.FIXED.20240314.gzip", sep='\t', header=0, compression='gzip',
    usecols=["phe1_name", "phe2_name", "gcor", "gcor_SE", "zscore", "P"]
)

# df_ToPlot_BBJ = pd.read_excel("data/SupplementaryTable2.xlsx", header=0)
df_ToPlot_BBJ = pd.read_csv("/home/wschoi/webapp_test/data/SupplementaryTable2.gzip", sep='\t', header=0, compression='gzip',)


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



##### [1] Web-page components

####### [1-1] the main navigation bar #####

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



####### [1-2] link page: "Review" #####

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



####### [1-3] link page: "Home" #####

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



####### [1-4] link page: "About" #####

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


####### [1-5] link page: "BBJ" #####

def create_link_page_BBJ(_fig_UMAP_BBJ, _df_ToPlot_BBJ, _df_rg_BBJ):
    
    ##### Sidebar
    sidebar = html.Div(
        [
            html.H2("Contents", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Community detection result", href="#community_BBJ", className="nav-link", external_link=True),
                    dbc.NavLink("UMAP", href="#umap_BBJ", className="nav-link", external_link=True),
                    dbc.NavLink([html.Span(["Estimated r", html.Sub("g"), " of a pair of traits by LDSC."])],
                                href="#rg_LDSC_BBJ", className="nav-link", external_link=True),
                    dbc.NavLink([html.Span(["Estimated r", html.Sub("g"), " on the UMAP"])], 
                                href="#estimated_rg_BBJ", className="nav-link", external_link=True),                    
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
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]

    ### [2] UMAP
    content_UMAP = [
        html.H2("UMAP", id="umap_BBJ"),
        html.P("This is the UMAP content for BBJ.", style={'font-family': 'Arial'}),
        html.Div([
            html.Div(dcc.Graph(id='UMAP_BBJ', figure=_fig_UMAP_BBJ), style={'display': 'flex', 'justifyContent': 'center'})
        ], style={'width': '100%'}),
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]
    
    
    ### [3] rg by LDSC
    options = [
        f"({_phe_id}) {_description}" for _idx, _phe_id, _description in _df_ToPlot_BBJ[['phe_name_dir (BBJ)', 'phenostring (BBJ)']].itertuples()
    ]

    content_rg_LDSC = [
        html.H2(id="rg_LDSC_BBJ", children=["Estimated ", html.I("r"), html.Sub("g"), " of a pair of traits by LDSC."]),
        html.P("You can check a pair of traits' estimated genetic correlation value here.", style={'font-family': 'Arial'}),
    
        # Datalist that provides the options 
        html.Datalist(id="trait-list_BBJ", children=[html.Option(value=opt) for opt in options]),

        ### Trait 1
        dcc.Input(id="input-trait1_BBJ", list="trait-list_BBJ", type="text", placeholder="Select trait 1", style={'width': '80%'}),
        html.Div(style={"height": "20px"}),
        
        ### Trait 2
        dcc.Input(id="input-trait2_BBJ", list="trait-list_BBJ", type="text", placeholder="Select trait 2", style={'width': '80%'}),
        html.Div(style={"height": "20px"}),

        ### Genetic correlation 정보
        html.Button("Submit", id='submit-button_BBJ', n_clicks=0),
        
        html.Div(style={"height": "20px"}),  
        
        # 선택된 trait pair에 해당하는 데이터 표시
        dcc.Markdown(id='trait-pair-output_BBJ', style={'font-family': 'Arial'}),
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]    
    
    
    ### [4] UMAP_rg
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
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]    

    ### [5] tSNE
    content_tSNE = [
        html.H2("tSNE", id="tsne_BBJ"),
        html.P("This is the tSNE content for BBJ.", style={'font-family': 'Arial'}),
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]

    
    ##### Wrap-up
    
    l_contents = [content_CM, content_UMAP, content_rg_LDSC, content_UMAP_rg, content_tSNE]

    def extend_contents(x: list, y: list) -> list:
        x.extend(y)
        return x
    
    l_contents = reduce(lambda x, y: extend_contents(x, y), l_contents)
    
    content = html.Div(
        l_contents,
        style={"margin-left": "270px", "padding": "20px"},
    )
    
    return sidebar, content



####### [1-6] link page: "UKBB" #####

def create_link_page_UKBB(_fig_UMAP_UKBB, _df_ToPlot_UKBB, _df_rg_UKBB):
    
    ##### Sidebar
    sidebar = html.Div(
        [
            html.H2("Contents", className="display-4"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Community detection result", href="#community_UKBB", className="nav-link", external_link=True),
                    dbc.NavLink("UMAP", href="#umap_UKBB", className="nav-link", external_link=True),
                    dbc.NavLink([html.Span(["Estimated r", html.Sub("g"), " of a pair of traits by LDSC."])],
                                href="#rg_LDSC_UKBB", className="nav-link", external_link=True),
                    dbc.NavLink([html.Span(["Estimated r", html.Sub("g"), " on the UMAP"])],
                                href="#estimated_rg_UKBB", className="nav-link", external_link=True),
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
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]

    ### [2] UMAP
    content_UMAP = [
        html.H2("UMAP", id="umap_UKBB"),
        html.P("This is the UMAP content for UKBB.", style={'font-family': 'Arial'}),
        html.Div([
            html.Div(dcc.Graph(id='UMAP_UKBB', figure=_fig_UMAP_UKBB), style={'display': 'flex', 'justifyContent': 'center'})
        ], style={'width': '100%'}),
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]
    
    ### [3] rg by LDSC
    # options = _df_rg_UKBB['phe1_name'].unique()
    # options = _df_ToPlot_UKBB['Description'].unique()
    options = [
        f"({_phe_id}) {_description}" for _idx, _phe_id, _description in _df_ToPlot_UKBB[['Phenocode_nealelab', 'Description']].itertuples()
    ]



    content_rg_LDSC = [
        html.H2(id="rg_LDSC_UKBB", children=["Estimated ", html.I("r"), html.Sub("g"), " of a pair of traits by LDSC."]),
        html.P("You can check a pair of traits' estimated genetic correlation value here.", style={'font-family': 'Arial'}),
    
        # Datalist that provides the options 
        html.Datalist(id="trait-list_UKBB", children=[html.Option(value=opt) for opt in options]),

        ### Trait 1
        dcc.Input(id="input-trait1_UKBB", list="trait-list_UKBB", type="text", placeholder="Select trait 1", style={'width': '80%'}),
        html.Div(style={"height": "20px"}),  


        ### Trait 2
        dcc.Input(id="input-trait2_UKBB", list="trait-list_UKBB", type="text", placeholder="Select trait 2", style={'width': '80%'}),
        html.Div(style={"height": "20px"}),  


        ### Genetic correlation 정보
        html.Button("Submit", id='submit-button_UKBB', n_clicks=0),
        
        html.Div(style={"height": "20px"}),  
        
        # 선택된 trait pair에 해당하는 데이터 표시
        dcc.Markdown(id='trait-pair-output_UKBB', style={'font-family': 'Arial'}),
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]

    

    ### [4] UMAP_rg
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
            filter_options={"case": "insensitive"} # , "placeholder_text": "Filter column..."
        ),    
        html.Div(id='clicked-cell', style={'marginTop': '20px'}),  # 클릭된 셀 값을 표시할 Div 추가
        html.Div(id='UMAP_rg_div'),  # UMAP을 표시할 Div 추가
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]    

    ### [5] tSNE
    content_tSNE = [
        html.H2("tSNE", id="tsne_UKBB"),
        html.P("This is the tSNE content for UKBB.", style={'font-family': 'Arial'}),
        html.Div(style={"height": "100px"}),  # 여백 추가
    ]

    
    ##### Wrap-up
    
    l_contents = [content_CM, content_UMAP, content_rg_LDSC, content_UMAP_rg, content_tSNE]

    def extend_contents(x: list, y: list) -> list:
        x.extend(y)
        return x
    
    l_contents = reduce(lambda x, y: extend_contents(x, y), l_contents)
    
    content = html.Div(
        l_contents,
        style={"margin-left": "270px", "padding": "20px"},
    )
    
    return sidebar, content


##### [2] Callback functions #####

###### [2-0] 대시보드 레이아웃 설정

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
        sidebar, content = create_link_page_UKBB(fig_UMAP_UKBB, df_ToPlot_UKBB, df_rg_UKBB)
    elif pathname == '/bbj':
        sidebar, content = create_link_page_BBJ(fig_UMAP_BBJ, df_ToPlot_BBJ, df_rg_BBJ)
    elif pathname == '/review':
        sidebar, content = create_link_page_Review()
    elif pathname == '/about':
        sidebar, content = create_link_page_About()
    else:
        sidebar, content = create_link_page_Home()

    return navbar, sidebar, content



###### [2-1 / UKBB] 클릭된 셀의 값을 가져와서 UMAP을 업데이트하는 콜백 함수

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



###### [2-1 / BBJ] 클릭된 셀의 값을 가져와서 UMAP을 업데이트하는 콜백 함수

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



###### [2-2] Navlink Javascript로 구현한거.

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



###### [2-3 / UKBB] LDSC rg 보여주는 부분.

@app.callback(
    Output('trait-pair-output_UKBB', 'children'),
    Input('submit-button_UKBB', 'n_clicks'),
    [Input('input-trait1_UKBB', 'value'), Input('input-trait2_UKBB', 'value')]
)
def show_trait_pair_data_UKBB(n_clicks, _trait_1, _trait_2):
    
    """
    (2024.09.09.)
    - df_rg_UMAP 이런걸 argument로 받을라 켔는데, 생각보다 복잡함. (State이런거 거쳐야 함.)
    - 이럴바에는 그냥 global로 받는게 훨씬 편하단걸 깨달음.
    - 어차피 webapp규모가 큰 것도 아니고 그냥 callback함수만 global로 가져다쓰는 방식으로 짜게.
    """    
    
    if n_clicks > 0 and _trait_1 and _trait_2:
        
        p_phe_id = re.compile(r'^\((\S+)\)\s+')

        m_trait_1 = p_phe_id.match(_trait_1)
        m_trait_2 = p_phe_id.match(_trait_2)

        if not m_trait_1:
            return "Given trait is strange. ({})".format(_trait_1)
        if not m_trait_2:
            return "Given trait is strange. ({})".format(_trait_2)

            
        _trait_1 = m_trait_1.group(1)
        _trait_2 = m_trait_2.group(1)
        
        f_pair = (df_rg_UKBB['phe1_name'] == _trait_1) & (df_rg_UKBB['phe2_name'] == _trait_2) | \
                (df_rg_UKBB['phe1_name'] == _trait_2) & (df_rg_UKBB['phe2_name'] == _trait_1)
        
        if f_pair.any():
            # if not matched_data.empty:
            
            matched_data = df_rg_UKBB[f_pair]
            # display(matched_data)

            matched_data = matched_data.to_dict('records')[0] # rows는 하나일거라 가정.
            gcor = matched_data['gcor']
            gcor_SE = matched_data['gcor_SE']
            zscore = matched_data['zscore']
            P = matched_data['P']
            
            str_RETURN = f"**{_trait_1}** and **{_trait_2}**:  \n" + \
                         f"- rg: {gcor}  \n" + \
                         f"- rg_SE: {gcor_SE}  \n" + \
                         f"- rg_zscore: {zscore}  \n" + \
                         f"- rg_pvalue: {P}"            

            
            return str_RETURN
        
        else:
            return "No data found for this trait pair."
        
    return "Please select two traits."



###### [2-3 / BBJ] LDSC rg 보여주는 부분.

@app.callback(
    Output('trait-pair-output_BBJ', 'children'),
    Input('submit-button_BBJ', 'n_clicks'),
    [Input('input-trait1_BBJ', 'value'), Input('input-trait2_BBJ', 'value')]
)
def show_trait_pair_data_BBJ(n_clicks, _trait_1, _trait_2):
    
    if n_clicks > 0 and _trait_1 and _trait_2:
        
        p_phe_id = re.compile(r'^\((\S+)\)\s+')

        m_trait_1 = p_phe_id.match(_trait_1)
        m_trait_2 = p_phe_id.match(_trait_2)

        if not m_trait_1:
            return "Given trait is strange. ({})".format(_trait_1)
        if not m_trait_2:
            return "Given trait is strange. ({})".format(_trait_2)

            
        _trait_1 = m_trait_1.group(1)
        _trait_2 = m_trait_2.group(1)
        
        f_pair = (df_rg_BBJ['phe1_name'] == _trait_1) & (df_rg_BBJ['phe2_name'] == _trait_2) | \
                (df_rg_BBJ['phe1_name'] == _trait_2) & (df_rg_BBJ['phe2_name'] == _trait_1)
        
        if f_pair.any():
            # if not matched_data.empty:
            
            matched_data = df_rg_BBJ[f_pair]
            # display(matched_data)

            matched_data = matched_data.to_dict('records')[0] # rows는 하나일거라 가정.
            gcor = matched_data['gcor']
            gcor_SE = matched_data['gcor_SE']
            zscore = matched_data['zscore']
            P = matched_data['P']
            
            str_RETURN = f"**{_trait_1}** and **{_trait_2}**:  \n" + \
                         f"- rg: {gcor}  \n" + \
                         f"- rg_SE: {gcor_SE}  \n" + \
                         f"- rg_zscore: {zscore}  \n" + \
                         f"- rg_pvalue: {P}"            

            
            return str_RETURN
        
        else:
            return "No data found for this trait pair."
        
    return "Please select two traits."






# 대시보드 서버 실행
if __name__ == '__main__':
    app.run_server(debug=False)
