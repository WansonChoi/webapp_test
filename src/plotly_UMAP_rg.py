import os, sys, re
# import numpy as np
import pandas as pd
from functools import reduce

import plotly.express as px
# import matplotlib.pyplot as plt


plotly_colorscale = \
[(0.0, 'rgba(142, 1, 82, 1.0)'),
 (0.00392156862745098, 'rgba(144, 2, 83, 1.0)'),
 (0.00784313725490196, 'rgba(146, 3, 85, 1.0)'),
 (0.011764705882352941, 'rgba(148, 4, 87, 1.0)'),
 (0.01568627450980392, 'rgba(150, 5, 88, 1.0)'),
 (0.0196078431372549, 'rgba(152, 6, 90, 1.0)'),
 (0.023529411764705882, 'rgba(154, 7, 92, 1.0)'),
 (0.027450980392156862, 'rgba(157, 8, 93, 1.0)'),
 (0.03137254901960784, 'rgba(159, 9, 95, 1.0)'),
 (0.03529411764705882, 'rgba(161, 10, 97, 1.0)'),
 (0.0392156862745098, 'rgba(163, 11, 98, 1.0)'),
 (0.043137254901960784, 'rgba(165, 12, 100, 1.0)'),
 (0.047058823529411764, 'rgba(167, 13, 102, 1.0)'),
 (0.050980392156862744, 'rgba(170, 14, 103, 1.0)'),
 (0.054901960784313725, 'rgba(172, 15, 105, 1.0)'),
 (0.058823529411764705, 'rgba(174, 16, 107, 1.0)'),
 (0.06274509803921569, 'rgba(176, 17, 108, 1.0)'),
 (0.06666666666666667, 'rgba(178, 18, 110, 1.0)'),
 (0.07058823529411765, 'rgba(180, 19, 112, 1.0)'),
 (0.07450980392156863, 'rgba(182, 20, 114, 1.0)'),
 (0.0784313725490196, 'rgba(185, 21, 115, 1.0)'),
 (0.08235294117647059, 'rgba(187, 22, 117, 1.0)'),
 (0.08627450980392157, 'rgba(189, 23, 119, 1.0)'),
 (0.09019607843137255, 'rgba(191, 24, 120, 1.0)'),
 (0.09411764705882353, 'rgba(193, 25, 122, 1.0)'),
 (0.09803921568627451, 'rgba(195, 26, 124, 1.0)'),
 (0.10196078431372549, 'rgba(197, 28, 125, 1.0)'),
 (0.10588235294117647, 'rgba(198, 32, 127, 1.0)'),
 (0.10980392156862745, 'rgba(199, 36, 129, 1.0)'),
 (0.11372549019607843, 'rgba(200, 39, 131, 1.0)'),
 (0.11764705882352941, 'rgba(201, 43, 133, 1.0)'),
 (0.12156862745098039, 'rgba(202, 46, 135, 1.0)'),
 (0.12549019607843137, 'rgba(203, 50, 137, 1.0)'),
 (0.12941176470588237, 'rgba(204, 54, 139, 1.0)'),
 (0.13333333333333333, 'rgba(205, 57, 141, 1.0)'),
 (0.13725490196078433, 'rgba(206, 61, 143, 1.0)'),
 (0.1411764705882353, 'rgba(207, 64, 145, 1.0)'),
 (0.1450980392156863, 'rgba(208, 68, 147, 1.0)'),
 (0.14901960784313725, 'rgba(209, 72, 149, 1.0)'),
 (0.15294117647058825, 'rgba(210, 75, 150, 1.0)'),
 (0.1568627450980392, 'rgba(211, 79, 152, 1.0)'),
 (0.1607843137254902, 'rgba(212, 82, 154, 1.0)'),
 (0.16470588235294117, 'rgba(213, 86, 156, 1.0)'),
 (0.16862745098039217, 'rgba(214, 90, 158, 1.0)'),
 (0.17254901960784313, 'rgba(215, 93, 160, 1.0)'),
 (0.17647058823529413, 'rgba(216, 97, 162, 1.0)'),
 (0.1803921568627451, 'rgba(217, 100, 164, 1.0)'),
 (0.1843137254901961, 'rgba(218, 104, 166, 1.0)'),
 (0.18823529411764706, 'rgba(219, 108, 168, 1.0)'),
 (0.19215686274509805, 'rgba(220, 111, 170, 1.0)'),
 (0.19607843137254902, 'rgba(221, 115, 172, 1.0)'),
 (0.2, 'rgba(222, 119, 174, 1.0)'),
 (0.20392156862745098, 'rgba(222, 121, 175, 1.0)'),
 (0.20784313725490197, 'rgba(223, 123, 177, 1.0)'),
 (0.21176470588235294, 'rgba(224, 126, 179, 1.0)'),
 (0.21568627450980393, 'rgba(224, 128, 180, 1.0)'),
 (0.2196078431372549, 'rgba(225, 131, 182, 1.0)'),
 (0.2235294117647059, 'rgba(226, 133, 184, 1.0)'),
 (0.22745098039215686, 'rgba(227, 136, 186, 1.0)'),
 (0.23137254901960785, 'rgba(227, 138, 187, 1.0)'),
 (0.23529411764705882, 'rgba(228, 141, 189, 1.0)'),
 (0.23921568627450981, 'rgba(229, 143, 191, 1.0)'),
 (0.24313725490196078, 'rgba(230, 146, 192, 1.0)'),
 (0.24705882352941178, 'rgba(230, 148, 194, 1.0)'),
 (0.25098039215686274, 'rgba(231, 151, 196, 1.0)'),
 (0.2549019607843137, 'rgba(232, 153, 198, 1.0)'),
 (0.25882352941176473, 'rgba(233, 156, 199, 1.0)'),
 (0.2627450980392157, 'rgba(233, 158, 201, 1.0)'),
 (0.26666666666666666, 'rgba(234, 161, 203, 1.0)'),
 (0.27058823529411763, 'rgba(235, 163, 205, 1.0)'),
 (0.27450980392156865, 'rgba(236, 165, 206, 1.0)'),
 (0.2784313725490196, 'rgba(236, 168, 208, 1.0)'),
 (0.2823529411764706, 'rgba(237, 170, 210, 1.0)'),
 (0.28627450980392155, 'rgba(238, 173, 211, 1.0)'),
 (0.2901960784313726, 'rgba(239, 175, 213, 1.0)'),
 (0.29411764705882354, 'rgba(239, 178, 215, 1.0)'),
 (0.2980392156862745, 'rgba(240, 180, 217, 1.0)'),
 (0.30196078431372547, 'rgba(241, 182, 218, 1.0)'),
 (0.3058823529411765, 'rgba(241, 184, 219, 1.0)'),
 (0.30980392156862746, 'rgba(242, 186, 220, 1.0)'),
 (0.3137254901960784, 'rgba(242, 187, 220, 1.0)'),
 (0.3176470588235294, 'rgba(243, 189, 221, 1.0)'),
 (0.3215686274509804, 'rgba(243, 191, 222, 1.0)'),
 (0.3254901960784314, 'rgba(244, 192, 223, 1.0)'),
 (0.32941176470588235, 'rgba(244, 194, 224, 1.0)'),
 (0.3333333333333333, 'rgba(245, 195, 225, 1.0)'),
 (0.33725490196078434, 'rgba(245, 197, 225, 1.0)'),
 (0.3411764705882353, 'rgba(245, 199, 226, 1.0)'),
 (0.34509803921568627, 'rgba(246, 200, 227, 1.0)'),
 (0.34901960784313724, 'rgba(246, 202, 228, 1.0)'),
 (0.35294117647058826, 'rgba(247, 204, 229, 1.0)'),
 (0.3568627450980392, 'rgba(247, 205, 229, 1.0)'),
 (0.3607843137254902, 'rgba(248, 207, 230, 1.0)'),
 (0.36470588235294116, 'rgba(248, 209, 231, 1.0)'),
 (0.3686274509803922, 'rgba(249, 210, 232, 1.0)'),
 (0.37254901960784315, 'rgba(249, 212, 233, 1.0)'),
 (0.3764705882352941, 'rgba(250, 214, 234, 1.0)'),
 (0.3803921568627451, 'rgba(250, 215, 234, 1.0)'),
 (0.3843137254901961, 'rgba(251, 217, 235, 1.0)'),
 (0.38823529411764707, 'rgba(251, 219, 236, 1.0)'),
 (0.39215686274509803, 'rgba(252, 220, 237, 1.0)'),
 (0.396078431372549, 'rgba(252, 222, 238, 1.0)'),
 (0.4, 'rgba(253, 224, 239, 1.0)'),
 (0.403921568627451, 'rgba(252, 224, 239, 1.0)'),
 (0.40784313725490196, 'rgba(252, 225, 239, 1.0)'),
 (0.4117647058823529, 'rgba(252, 226, 239, 1.0)'),
 (0.41568627450980394, 'rgba(252, 227, 240, 1.0)'),
 (0.4196078431372549, 'rgba(251, 228, 240, 1.0)'),
 (0.4235294117647059, 'rgba(251, 229, 240, 1.0)'),
 (0.42745098039215684, 'rgba(251, 230, 241, 1.0)'),
 (0.43137254901960786, 'rgba(251, 231, 241, 1.0)'),
 (0.43529411764705883, 'rgba(250, 232, 241, 1.0)'),
 (0.4392156862745098, 'rgba(250, 233, 242, 1.0)'),
 (0.44313725490196076, 'rgba(250, 233, 242, 1.0)'),
 (0.4470588235294118, 'rgba(250, 234, 242, 1.0)'),
 (0.45098039215686275, 'rgba(249, 235, 243, 1.0)'),
 (0.4549019607843137, 'rgba(249, 236, 243, 1.0)'),
 (0.4588235294117647, 'rgba(249, 237, 243, 1.0)'),
 (0.4627450980392157, 'rgba(249, 238, 244, 1.0)'),
 (0.4666666666666667, 'rgba(249, 239, 244, 1.0)'),
 (0.47058823529411764, 'rgba(248, 240, 244, 1.0)'),
 (0.4745098039215686, 'rgba(248, 241, 244, 1.0)'),
 (0.47843137254901963, 'rgba(248, 242, 245, 1.0)'),
 (0.4823529411764706, 'rgba(248, 242, 245, 1.0)'),
 (0.48627450980392156, 'rgba(247, 243, 245, 1.0)'),
 (0.49019607843137253, 'rgba(247, 244, 246, 1.0)'),
 (0.49411764705882355, 'rgba(247, 245, 246, 1.0)'),
 (0.4980392156862745, 'rgba(247, 246, 246, 1.0)'),
 (0.5019607843137255, 'rgba(246, 246, 246, 1.0)'),
 (0.5058823529411764, 'rgba(246, 246, 244, 1.0)'),
 (0.5098039215686274, 'rgba(245, 246, 243, 1.0)'),
 (0.5137254901960784, 'rgba(244, 246, 241, 1.0)'),
 (0.5176470588235295, 'rgba(244, 246, 240, 1.0)'),
 (0.5215686274509804, 'rgba(243, 246, 238, 1.0)'),
 (0.5254901960784314, 'rgba(242, 246, 237, 1.0)'),
 (0.5294117647058824, 'rgba(242, 246, 235, 1.0)'),
 (0.5333333333333333, 'rgba(241, 246, 234, 1.0)'),
 (0.5372549019607843, 'rgba(240, 246, 232, 1.0)'),
 (0.5411764705882353, 'rgba(240, 246, 230, 1.0)'),
 (0.5450980392156862, 'rgba(239, 246, 229, 1.0)'),
 (0.5490196078431373, 'rgba(238, 246, 227, 1.0)'),
 (0.5529411764705883, 'rgba(238, 245, 226, 1.0)'),
 (0.5568627450980392, 'rgba(237, 245, 224, 1.0)'),
 (0.5607843137254902, 'rgba(236, 245, 223, 1.0)'),
 (0.5647058823529412, 'rgba(236, 245, 221, 1.0)'),
 (0.5686274509803921, 'rgba(235, 245, 220, 1.0)'),
 (0.5725490196078431, 'rgba(234, 245, 218, 1.0)'),
 (0.5764705882352941, 'rgba(234, 245, 217, 1.0)'),
 (0.5803921568627451, 'rgba(233, 245, 215, 1.0)'),
 (0.5843137254901961, 'rgba(232, 245, 214, 1.0)'),
 (0.5882352941176471, 'rgba(232, 245, 212, 1.0)'),
 (0.592156862745098, 'rgba(231, 245, 211, 1.0)'),
 (0.596078431372549, 'rgba(230, 245, 209, 1.0)'),
 (0.6, 'rgba(230, 245, 208, 1.0)'),
 (0.6039215686274509, 'rgba(228, 244, 205, 1.0)'),
 (0.6078431372549019, 'rgba(226, 243, 202, 1.0)'),
 (0.611764705882353, 'rgba(224, 242, 199, 1.0)'),
 (0.615686274509804, 'rgba(222, 241, 196, 1.0)'),
 (0.6196078431372549, 'rgba(220, 241, 193, 1.0)'),
 (0.6235294117647059, 'rgba(219, 240, 190, 1.0)'),
 (0.6274509803921569, 'rgba(217, 239, 187, 1.0)'),
 (0.6313725490196078, 'rgba(215, 238, 184, 1.0)'),
 (0.6352941176470588, 'rgba(213, 237, 181, 1.0)'),
 (0.6392156862745098, 'rgba(211, 237, 178, 1.0)'),
 (0.6431372549019608, 'rgba(210, 236, 176, 1.0)'),
 (0.6470588235294118, 'rgba(208, 235, 173, 1.0)'),
 (0.6509803921568628, 'rgba(206, 234, 170, 1.0)'),
 (0.6549019607843137, 'rgba(204, 234, 167, 1.0)'),
 (0.6588235294117647, 'rgba(202, 233, 164, 1.0)'),
 (0.6627450980392157, 'rgba(201, 232, 161, 1.0)'),
 (0.6666666666666666, 'rgba(199, 231, 158, 1.0)'),
 (0.6705882352941176, 'rgba(197, 230, 155, 1.0)'),
 (0.6745098039215687, 'rgba(195, 230, 152, 1.0)'),
 (0.6784313725490196, 'rgba(193, 229, 149, 1.0)'),
 (0.6823529411764706, 'rgba(192, 228, 147, 1.0)'),
 (0.6862745098039216, 'rgba(190, 227, 144, 1.0)'),
 (0.6901960784313725, 'rgba(188, 226, 141, 1.0)'),
 (0.6941176470588235, 'rgba(186, 226, 138, 1.0)'),
 (0.6980392156862745, 'rgba(184, 225, 135, 1.0)'),
 (0.7019607843137254, 'rgba(182, 224, 132, 1.0)'),
 (0.7058823529411765, 'rgba(180, 222, 129, 1.0)'),
 (0.7098039215686275, 'rgba(178, 221, 127, 1.0)'),
 (0.7137254901960784, 'rgba(176, 219, 124, 1.0)'),
 (0.7176470588235294, 'rgba(173, 218, 121, 1.0)'),
 (0.7215686274509804, 'rgba(171, 217, 119, 1.0)'),
 (0.7254901960784313, 'rgba(169, 215, 116, 1.0)'),
 (0.7294117647058823, 'rgba(167, 214, 113, 1.0)'),
 (0.7333333333333333, 'rgba(165, 212, 111, 1.0)'),
 (0.7372549019607844, 'rgba(162, 211, 108, 1.0)'),
 (0.7411764705882353, 'rgba(160, 209, 105, 1.0)'),
 (0.7450980392156863, 'rgba(158, 208, 102, 1.0)'),
 (0.7490196078431373, 'rgba(156, 206, 100, 1.0)'),
 (0.7529411764705882, 'rgba(153, 205, 97, 1.0)'),
 (0.7568627450980392, 'rgba(151, 203, 94, 1.0)'),
 (0.7607843137254902, 'rgba(149, 202, 92, 1.0)'),
 (0.7647058823529411, 'rgba(147, 201, 89, 1.0)'),
 (0.7686274509803922, 'rgba(144, 199, 86, 1.0)'),
 (0.7725490196078432, 'rgba(142, 198, 83, 1.0)'),
 (0.7764705882352941, 'rgba(140, 196, 81, 1.0)'),
 (0.7803921568627451, 'rgba(138, 195, 78, 1.0)'),
 (0.7843137254901961, 'rgba(135, 193, 75, 1.0)'),
 (0.788235294117647, 'rgba(133, 192, 73, 1.0)'),
 (0.792156862745098, 'rgba(131, 190, 70, 1.0)'),
 (0.796078431372549, 'rgba(129, 189, 67, 1.0)'),
 (0.8, 'rgba(127, 188, 65, 1.0)'),
 (0.803921568627451, 'rgba(125, 186, 63, 1.0)'),
 (0.807843137254902, 'rgba(123, 184, 62, 1.0)'),
 (0.8117647058823529, 'rgba(121, 183, 61, 1.0)'),
 (0.8156862745098039, 'rgba(119, 181, 59, 1.0)'),
 (0.8196078431372549, 'rgba(117, 179, 58, 1.0)'),
 (0.8235294117647058, 'rgba(115, 178, 57, 1.0)'),
 (0.8274509803921568, 'rgba(113, 176, 56, 1.0)'),
 (0.8313725490196079, 'rgba(111, 174, 54, 1.0)'),
 (0.8352941176470589, 'rgba(109, 173, 53, 1.0)'),
 (0.8392156862745098, 'rgba(107, 171, 52, 1.0)'),
 (0.8431372549019608, 'rgba(105, 169, 51, 1.0)'),
 (0.8470588235294118, 'rgba(103, 168, 49, 1.0)'),
 (0.8509803921568627, 'rgba(101, 166, 48, 1.0)'),
 (0.8549019607843137, 'rgba(99, 164, 47, 1.0)'),
 (0.8588235294117647, 'rgba(97, 163, 46, 1.0)'),
 (0.8627450980392157, 'rgba(95, 161, 44, 1.0)'),
 (0.8666666666666667, 'rgba(93, 160, 43, 1.0)'),
 (0.8705882352941177, 'rgba(91, 158, 42, 1.0)'),
 (0.8745098039215686, 'rgba(89, 156, 41, 1.0)'),
 (0.8784313725490196, 'rgba(87, 155, 39, 1.0)'),
 (0.8823529411764706, 'rgba(85, 153, 38, 1.0)'),
 (0.8862745098039215, 'rgba(83, 151, 37, 1.0)'),
 (0.8901960784313725, 'rgba(81, 150, 36, 1.0)'),
 (0.8941176470588236, 'rgba(79, 148, 34, 1.0)'),
 (0.8980392156862745, 'rgba(77, 146, 33, 1.0)'),
 (0.9019607843137255, 'rgba(76, 145, 32, 1.0)'),
 (0.9058823529411765, 'rgba(74, 143, 32, 1.0)'),
 (0.9098039215686274, 'rgba(73, 141, 32, 1.0)'),
 (0.9137254901960784, 'rgba(71, 139, 31, 1.0)'),
 (0.9176470588235294, 'rgba(70, 137, 31, 1.0)'),
 (0.9215686274509803, 'rgba(68, 136, 31, 1.0)'),
 (0.9254901960784314, 'rgba(67, 134, 30, 1.0)'),
 (0.9294117647058824, 'rgba(65, 132, 30, 1.0)'),
 (0.9333333333333333, 'rgba(64, 130, 30, 1.0)'),
 (0.9372549019607843, 'rgba(62, 128, 30, 1.0)'),
 (0.9411764705882353, 'rgba(61, 127, 29, 1.0)'),
 (0.9450980392156862, 'rgba(59, 125, 29, 1.0)'),
 (0.9490196078431372, 'rgba(58, 123, 29, 1.0)'),
 (0.9529411764705882, 'rgba(56, 121, 28, 1.0)'),
 (0.9568627450980393, 'rgba(55, 119, 28, 1.0)'),
 (0.9607843137254902, 'rgba(53, 118, 28, 1.0)'),
 (0.9647058823529412, 'rgba(52, 116, 27, 1.0)'),
 (0.9686274509803922, 'rgba(50, 114, 27, 1.0)'),
 (0.9725490196078431, 'rgba(49, 112, 27, 1.0)'),
 (0.9764705882352941, 'rgba(47, 110, 26, 1.0)'),
 (0.9803921568627451, 'rgba(46, 109, 26, 1.0)'),
 (0.984313725490196, 'rgba(44, 107, 26, 1.0)'),
 (0.9882352941176471, 'rgba(43, 105, 25, 1.0)'),
 (0.9921568627450981, 'rgba(41, 103, 25, 1.0)'),
 (0.996078431372549, 'rgba(40, 101, 25, 1.0)'),
 (1.0, 'rgba(39, 100, 25, 1.0)')]

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
    
    # cmap = plt.get_cmap('PiYG')
    # colors = [cmap(i) for i in range(cmap.N)]
    # plotly_colorscale = [(i / (cmap.N - 1), f'rgba({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)}, {c[3]})') for i, c in enumerate(colors)]
    


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