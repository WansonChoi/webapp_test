import os, sys, re
# import numpy as np
import pandas as pd
from functools import reduce

import plotly.express as px



def plotly_UMAP_main(_df_ToPlot, _cohort, _df_UMAP, _df_cmap, 
                     _figsize_pixel=(840, 800), 
                     _start_UMAP_xrange=(-40, 60), _start_UMAP_yrange=(-40, 60)):
    
    ### functions to use
    def preprocess_df_ToPlot_UKBB(_df_ToPlot, _df_UMAP):

        ##### 필요없는 columns들
        df_main = _df_ToPlot.drop(["Sub-cluster No.", "description_more (Pan-UKBB)"], axis=1)


        ##### [2] inner_join with UMAP
        df_main = _df_UMAP.reset_index(drop=False).merge(
            df_main.rename({"Phenocode_nealelab": "Phenotype"}, axis=1)
        )
        # display(df_main)

        # 어차피 inner_join하고 나서 뭘 해야함. (원래는 전처리할때 하려했었는데 여기서 하는게 훨씬 나음.)

        N_cluster_max = df_main['Cluster No.'].max()
        sr_ClusterNo_cat = df_main['Cluster No.'].astype(str).astype("category")
        sr_ClusterNo_cat = sr_ClusterNo_cat.cat.set_categories([str(_) for _ in range(1, N_cluster_max + 1)], ordered=True)
        # display(sr_ClusterNo_cat)

        df_main = pd.concat(
            [
                sr_ClusterNo_cat,
                df_main.drop(['Cluster No.'], axis=1),
            ],
            axis=1
        )
        
        return df_main, list(df_main['Cluster No.'].cat.categories)


    def preprocess_df_ToPlot_BBJ(_df_ToPlot, _df_UMAP):

        ##### 전처리 
        
        ### 필요없는 columns들
        df_main = _df_ToPlot.drop(["Sub-cluster No."], axis=1)
        
        ### variable type 변환.
        sr_variable_type = df_main['isBinary (BBJ)'].map(lambda x: "binary" if x else "continuous")
        
        ### isDisease column
        sr_isDisease = df_main['category (BBJ)'].map(lambda x: "Disease" if x.startswith("ICD10") else "Intermediate").rename("isDisease")
        
        df_main = pd.concat([
            df_main.drop(['isBinary (BBJ)'], axis=1), 
            sr_variable_type,
            sr_isDisease
        ], axis=1)
        
        ##### inner_join
        df_main = _df_UMAP.reset_index(drop=False).merge(
            df_main.rename({"phe_name_dir (BBJ)": "Phenotype"}, axis=1)
        )
        # display(df_main)
        
        ##### cluster no. category화 하기.
        N_cluster_max = df_main['Cluster No.'].max()
        sr_ClusterNo_cat = df_main['Cluster No.'].astype(str).astype("category")
        sr_ClusterNo_cat = sr_ClusterNo_cat.cat.set_categories([str(_) for _ in range(1, N_cluster_max + 1)], ordered=True)
        # display(sr_ClusterNo_cat)

        df_main = pd.concat(
            [
                sr_ClusterNo_cat,
                df_main.drop(['Cluster No.'], axis=1),
            ],
            axis=1
        )
        
        return df_main, list(df_main['Cluster No.'].cat.categories)


    
    ### ============
    
    ##### [1] prerequisite
    
    
    ## (1-1) ToPlot (결국 얘가 annotation정보)
    df_main, l_category_orders = preprocess_df_ToPlot_UKBB(_df_ToPlot, _df_UMAP) if _cohort == "UKBB" else preprocess_df_ToPlot_BBJ(_df_ToPlot, _df_UMAP)
    # display(df_main.head(3))
    
    ## (1-2) colors
    d_cmap = {_[1]: _[2] for _ in _df_cmap.itertuples()}
    

    

    ##### [3] Main plotting part.
    
    # l_custom_data = df_main
    
    fig_2d = px.scatter(
        df_main, x='UMAP_1', y='UMAP_2',
        color='Cluster No.', labels={'Cluster No.': 'Cluster No.'},
        color_discrete_map=d_cmap,
        category_orders = {'Cluster No.': l_category_orders},
        width=_figsize_pixel[0], height=_figsize_pixel[1],
        custom_data=df_main.columns.tolist()
        # hover_name='Description',
        # custom_data=['Description','isDisease (Manual)', 'variable_type']
    )
    

    ##### [4] hover_text

    if _cohort == "UKBB":
    
        _hovertemplate_trait_info = "<b>%{customdata[1]}: %{customdata[4]}</b><br>"

        _hovertemplate_classification = "Cluster No.=%{customdata[0]}<br>" + \
                                        "isDisease=%{customdata[5]}<br>" + \
                                        "Category=%{customdata[6]}<br>"

        _hovertemplate_etc = "variable_type=%{customdata[9]}<br>" + \
                             "source=%{customdata[10]}<br>" + \
                             "sex=%{customdata[11]}<br>"

        hovertemplates = "<br>".join([
            _hovertemplate_trait_info,
            _hovertemplate_classification,
            _hovertemplate_etc
        ])
        
    else: ### BBJ
        
        _hovertemplate_trait_info = "<b>%{customdata[1]}: %{customdata[5]}</b><br>"

        _hovertemplate_classification = "Cluster No.=%{customdata[0]}<br>" + \
                                        "isDisease=%{customdata[9]}<br>" + \
                                        "Category=%{customdata[7]}<br>"

        _hovertemplate_etc = "variable_type=%{customdata[8]}<br>"

        hovertemplates = "<br>".join([
            _hovertemplate_trait_info,
            _hovertemplate_classification,
            _hovertemplate_etc
        ])

    

    fig_2d.update_traces(
        hovertemplate = hovertemplates
    )    
    
    
    
    ##### [5] 시작할때 위치 조정.

    
    fig_2d.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    })

    fig_2d.update_xaxes(range=_start_UMAP_xrange)
    fig_2d.update_yaxes(range=_start_UMAP_yrange)
    
    # fig_2d.show() # (2024.09.01.) 이거 안 없애면 web-app킬때마다 tab생김.
    
    return fig_2d