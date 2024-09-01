import os, sys, re
# import numpy as np
import pandas as pd
from functools import reduce

import plotly.express as px
import matplotlib.pyplot as plt




def plotly_UMAP_rg(_df_UMAP, _df_rg, _target_trait, _df_ToPlot, _cohort, _figsize_pixel=(840, 800), 
                     _start_UMAP_xrange=(-40, 60), _start_UMAP_yrange=(-40, 60)):
    
    ##### (1) the target trait vs. The other traits간의 Rg value vector만들기.
    
    def get_df_rg_subset(_df_rg, _target_trait,
                         _colname_phe1="phe1_name", _colname_phe2="phe2_name"):

        # display(_df_rg)

        ### 일단 subset한번 (`_target_trait`을 포함하는 trait pairs들만.)

        f_phe1 = _df_rg[_colname_phe1] == _target_trait
        f_phe2 = _df_rg[_colname_phe2] == _target_trait

        df_rg_subset = _df_rg[f_phe1 | f_phe2]
        # display(df_rg_subset) # 얘의 row는 항상 715 or 220임.
        
        ### columns 2개만 여기서 만들어 나가야함.
        
        ## (1) 
        sr_phenotype = pd.Series(
            [_[1] if _[1] != _target_trait else _[2] for _ in df_rg_subset[[_colname_phe1, _colname_phe2]].itertuples()],
            index=df_rg_subset.index,
            name='Phenotype'
        )
        
        ## (2) 
        sr_NA_failed = ~df_rg_subset['gcor'].isna().rename("LDSC_succeeded")
        
        ## (3) NA as 0
        sr_gcor_NA_0 = df_rg_subset['gcor'].fillna(0.0).rename("gcor_NA_0")
        
        df_rg_subset = pd.concat([
            df_rg_subset,
            sr_phenotype,
            sr_NA_failed,
            sr_gcor_NA_0
        ], axis=1)
        
        return df_rg_subset
    
    df_rg_subset = get_df_rg_subset(_df_rg, _target_trait)
    # display(df_rg_subset)
    
    
    
    ##### (2) df_ToPlot 정리.
    
    def preprocess_df_ToPlot_UKBB(_df_ToPlot, _df_UMAP, _df_rg_subset):

        ##### 필요없는 columns들
        df_main = _df_ToPlot.drop([
            "Sub-cluster No.", "description_more (Pan-UKBB)", "category (Pan-UKBB)",
            "category_level 0 (Pan-UKBB)", "category_level 1 (Pan-UKBB)"], axis=1)


        ##### [2] inner_join with UMAP
        df_main = _df_UMAP.reset_index(drop=False).merge(
            df_main.rename({"Phenocode_nealelab": "Phenotype"}, axis=1)
        )
        # display(df_main)
        
        ##### [3] inner_join with rg_df
        df_rg_subset_2 = _df_rg_subset.drop(["id_phe1", "id_phe2", "phe1_name", "phe2_name"], axis=1)
        df_main = df_main.merge(df_rg_subset_2, on='Phenotype')
        # display(df_main)
        
        
        ## Cluster No.만 category로 만들기. (사실 필요 없음.)
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
    
    
    
    def preprocess_df_ToPlot_BBJ(_df_ToPlot, _df_UMAP, _df_rg_subset):

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
        
        
        ##### [2] inner_join
        df_main = _df_UMAP.reset_index(drop=False).merge(
            df_main.rename({"phe_name_dir (BBJ)": "Phenotype"}, axis=1)
        )
        # display(df_main)

        
        ##### [3] inner_join with rg_df
        df_rg_subset_2 = _df_rg_subset.drop(["id_phe1", "id_phe2", "phe1_name", "phe2_name"], axis=1, errors='ignore')
        # df_rg_subset_2 = _df_rg_subset.drop(["phe1_name", "phe2_name"], axis=1)
        df_main = df_main.merge(df_rg_subset_2, on='Phenotype')
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
    
    
    
    ##### Main
    
    df_main, l_categories_ordered = preprocess_df_ToPlot_UKBB(_df_ToPlot, _df_UMAP, df_rg_subset) if _cohort == "UKBB" else \
                                        preprocess_df_ToPlot_BBJ(_df_ToPlot, _df_UMAP, df_rg_subset)
    # display(df_main.head(3))
    # display(df_main.shape)

    
    
    
    ##### (Chat-gpt) Matplotlib colormap을 Plotly colormap으로 변환
    cmap = plt.get_cmap('PiYG')
    colors = [cmap(i) for i in range(cmap.N)]
    plotly_colorscale = [(i / (cmap.N - 1), f'rgba({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)}, {c[3]})') for i, c in enumerate(colors)]

    # display(cmap)
    # print(plotly_colorscale)
    
    
    ## Plotly scatter plot
    fig_2d = px.scatter(
        df_main, x='UMAP_1', y='UMAP_2',
        color="gcor_NA_0", 
        labels={'color': '<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>'},
        color_continuous_scale=plotly_colorscale,
        range_color=(-1, 1),  # Continuous values의 범위 지정
        width=_figsize_pixel[0], height=_figsize_pixel[1],
        # hover_name='Description',
        custom_data=df_main.columns
    )
    
    
    """
    (cf. 원래 기본으로 넣어주던거의 hovertemplate)
    UMAP_1=%{x}<br>UMAP_2=%{y}<br><span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>=%{marker.color}<extra></extra>    
    
    
    ## scatter에서 'hover_name'만 잡고, .update_traces()에서 다음의 hover_template을 쓰면 될 것 같음.
    - <b>%{hovertext}</b><br><br>UMAP_1=%{x}<br>UMAP_2=%{y}<br>rg_6152_8=%{marker.color}<extra></extra>
    - 핵심은 hovertext가 hover_name에 해당한다는거.
    
    # rg_part = f"rg_{_target_trait}" + "=%{marker.color}<br>"

    # _hovertemplate = \
    #     "<b>%{hovertext}</b><br><br>" + \
    #     rg_part + \
    #     "Cluster=%{customdata[0]}<br>" + \
    #     "variable_type=%{customdata[1]}<br>" + \
    #     "<br>UMAP_1=%{x}<br>" + \
    #     "UMAP_2=%{y}<br>" + \
    #     "<extra></extra>"    
    """
    
    if _cohort == "UKBB":
        
        _hovertemplate_trait_info = "<b>%{customdata[1]}: %{customdata[4]}</b><br>"
        
        _hvtemplate_rg = '<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>=%{marker.color}<br>'
        _hvtemplate_rg_se = '<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>_SE=%{customdata[11]}<br>'
        _hvtemplate_rg_zscore = '<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>_zscore=%{customdata[12]}<br>'
        _hvtemplate_rg_pvalue = '<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>_p-value=%{customdata[13]}<br>'
        _hvtemplate_rg_succeeded = 'LDSC_succeeded=%{customdata[14]}<br>'

        _hvtemplate_rg_summary = ''.join([_hvtemplate_rg, _hvtemplate_rg_se, _hvtemplate_rg_zscore, _hvtemplate_rg_pvalue, _hvtemplate_rg_succeeded])
        
        _hovertemplate_classification = "Cluster No.=%{customdata[0]}<br>" + \
                                        "isDisease=%{customdata[5]}<br>" + \
                                        "Category=%{customdata[6]}<br>"

        _hovertemplate_etc = "variable_type=%{customdata[7]}<br>" + \
                             "source=%{customdata[8]}<br>" + \
                             "sex=%{customdata[9]}<br>"
        
        
    else: ## BBJ.
        
        _hovertemplate_trait_info = "<b>%{customdata[1]}: %{customdata[5]}</b><br>"
        
        _hvtemplate_rg = '<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>=%{marker.color}<br>'
        _hvtemplate_rg_se = '<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>_SE=%{customdata[11]}<br>'
        _hvtemplate_rg_zscore = '<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>_zscore=%{customdata[12]}<br>'
        _hvtemplate_rg_pvalue = '<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>_p-value=%{customdata[13]}<br>'
        _hvtemplate_rg_succeeded = 'LDSC_succeeded=%{customdata[14]}<br>'

        _hvtemplate_rg_summary = ''.join([_hvtemplate_rg, _hvtemplate_rg_se, _hvtemplate_rg_zscore, _hvtemplate_rg_pvalue, _hvtemplate_rg_succeeded])
        
        _hovertemplate_classification = "Cluster No.=%{customdata[0]}<br>" + \
                                        "isDisease=%{customdata[9]}<br>" + \
                                        "Category=%{customdata[7]}<br>"

        _hovertemplate_etc = "variable_type=%{customdata[8]}<br>"
    
    
    
    hovertemplates = "<br>".join([
        _hovertemplate_trait_info,
        _hvtemplate_rg_summary,
        _hovertemplate_classification,
        _hovertemplate_etc
    ])
    
    fig_2d.update_traces(
        hovertemplate = hovertemplates
    )

    
    ##### Graph의 부가적인 부분 추가 수정.
    
    ## background 빼기
    fig_2d.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)'
    })

    ## colormap bar label 바꾸기.
    fig_2d.update_layout(
        coloraxis_colorbar=dict(
            title=dict(text='<span style="font-family:Cambria Math; font-style:italic;">r<sub>g</sub></span>', side='right')
        )
    )
    

    ## 시작 axis range바꾸기.
    fig_2d.update_xaxes(range=_start_UMAP_xrange)
    fig_2d.update_yaxes(range=_start_UMAP_yrange)
    
    # fig_2d.show()
    
    
    return fig_2d, df_main