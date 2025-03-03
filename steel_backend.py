
#from bokeh.plotting import figure
import math
import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image

language_dict = {"HUN":["Kihajlás", "Válasszon anyagminőséget!", "Válasszon keresztmetszetet!",
                        "Adja meg az elem hosszát! [mm]", "szélesség","magasság", "vastagság",
                        "keresztmetszeti terület", "inercia", "inercia erős tengely körül",
                        "inercia gyenge tengely körül", "anyagjellemzők", "geometria",
                        "igénybevételek", "számítás", "Beton anyagminősége",
                        "nyomószilárdság", "karakterisztikus", "értéke"],
                 "ENG": ["Buckling", "Choose a steel grade!", "Chosen section!",
                         "Set the length of the element! [mm]", "width", "height", "thickness",
                         "section area", "inertia", "inertia around the strong axis",
                         "inertia around the weak axis", "materials", "geometry", "internal forces",
                         "calculation", "Concrete material",
                         "compressive strength", "characteristic", "value"]}
language_list = list(language_dict.keys())

chosen_language = language_list[0]

steel_gamma = [1,1,1.25,1.25,1.1]

def set_language():
    return language_dict

df = pd.read_excel("section_table.xlsx", engine="openpyxl")

L_equal_name = df.iloc[:, 0].tolist()
L_equal_h = df.iloc[:, 1].tolist()
L_equal_t = df.iloc[:, 2].tolist()
L_equal_r1 = df.iloc[:, 3].tolist()
L_equal_r2 = df.iloc[:, 4].tolist()
L_equal_r3 = df.iloc[:, 5].tolist()
L_equal_r4 = df.iloc[:, 6].tolist()
L_equal_area = df.iloc[:, 7].tolist()
L_equal_inertia = df.iloc[:, 10].tolist()
L_equal_inertia_strong = df.iloc[:, 12].tolist()
L_equal_inertia_weak = df.iloc[:, 13].tolist()
L_equal_curve = df.iloc[:, -1].tolist()

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

L_equal_image_path = current_dir / "pics" / "L_equal.png"
L_equal_image = Image.open(L_equal_image_path)

steel_grade_dict = {"S235": [235, 360, 7850, 210000, 81000, 0,3, 0.000012],
              "S275": [275, 430, 7850, 210000, 81000, 0,3, 0.000012],
              "S355": [355, 490, 7850, 210000, 81000, 0,3, 0.000012],
              "S450": [440, 550, 7850, 210000, 81000, 0,3, 0.000012]}

steel_grade_list = list(steel_grade_dict.keys())

def get_Ncr (E, I, L):
    Ncr = ((math.pi**2)*E*I)/(L**2)
    return Ncr

def get_lambda (A, fy, Ncr):
    lambda_slender = math.sqrt(A*fy/Ncr)
    return lambda_slender

def get_imperfection_factor(buckling_curve):
    if str(buckling_curve) == "a0":
        return 0.13
    elif str(buckling_curve) == "a":
        return 0.21
    elif str(buckling_curve) == "b":
        return 0.34
    elif str(buckling_curve) == "c":
        return 0.49
    elif str(buckling_curve) == "d":
        return 0.76

def get_helping_factor(alpha, lambda_slender):
    phi = 0.5*(1+(alpha*(lambda_slender-0.2))+(lambda_slender**2))
    return phi

def get_reduction_factor(phi, lambda_slender):
    chi = min(1/(phi + math.sqrt(phi**2 - lambda_slender**2)),1)
    return chi

def get_buckling_resistance(chi, area, fy):
    Nbrd = chi * area * fy / steel_gamma[0]
    return Nbrd


# concrete_dict = {"C12/15":[12,15,8,0.73,1.6,1.6,3.02,27,6.7,0.4,0.00001],"C16/18":[16,18,10.7,0.89,1.9,2.0,2.76,29,7.7,0.4,0.00001],"C20/25":[20,25,13.3,1.0,2.2,2.3,2.55,30,8.5,0.4,0.00001],"C25/30":[25,30,16.7,1.2,2.6,2.7,2.35,31,9.3,0.4,0.00001],
#                  "C30/37":[30,37,20,1.4,2.9,3.0,2.13,33,10.5,0.4,0.00001],"C35/45":[35,40,23.3,1.5,3.2,3.4,1.92,34,11.6,0.4,0.00001],
#                  "C40/50":[40,50,26.7,1.6,3.5,3.7,1.76,35,12.7,0.4,0.00001],"C45/55": [45,55,30,1.8,3.8,4.0,1.63,36,13.7,0.4,0.00001],
#                  "C50/60": [50,60,33.3,1.9,4.1,4.3,1.53,37,14.6,0.4,0.00001]}
#
# bar_diameter_list = [6, 8, 10, 12, 14, 16, 20, 22, 25, 32]
#
# def return_bar_diameter_list():
#     return  bar_diameter_list
#
# concrete_name_list = list(concrete_dict.keys())
#
# gamma_concrete = 1.5
#
# strand_metal_dict = {"Y1770":[1770,195,3.5],"Y1860":[1860,195,3.5],"Y1920":[1920,195,3.5],"Y1960":[1960,195,3.5], "Y2060":[2060,195,3.5], "Y2160":[2160,195,3.5]}
#
# def get_strand_metal_dict():
#     return strand_metal_dict
#
# strand_1770_dict = {"1770S2-5,6":[2,5.6,9.7,75.8,17.2,19.8,14.8],"1770S2-6,0":[2,6.0,15.1,117.9,26.7,30.7,23.0],"1770S3-7,5":[3,7.5,29.0,226.5,51.3,59.0,44.1],"1770S7-6,9":[7,6.9,29.0,226.5,51.3,59.0,44.1],
#                     "1770S7-9,0":[7,9.0,50,390.5,88.5,102,76.1],"1770S7-9,3":[7,9.3,52,406.1,92,106,79.1],"1770S7-9,6":[7,9.6,55,429.6,97.4,112,83.8],
#                     "1770S7-11":[7,11.0,70,546.7,124,143,107],"1770S7-12,5":[7,12.5,93,726.3,165,190,142],"1770S7-12,9":[7,12.9,100,781,177,204,152],
#                     "1770S7-15,2":[7,15.2,139,1086,246,283,212],"1770S7-15,3":[7,15.3,140,1093,248,285,213],"1770S7-15,7":[7,15.7,150,1172,266,306,229],
#                     "1770S7-18,0":[7,18,200,1562,354,407,304]}
#
#
#
# strand_1860_dict = {"1860S2-4,5":[2,4.5,7.95,62.1,14.8,17.0,12.7], "1860S3-4,85":[3,4.85,11.9,92.9,22.1,25.4,19], "1860S3-6,5":[3,6.5,21.2,165.6,39.4,45.3,33.9],
#                     "1860S3-6,9":[3,6.9,23.4,182.8,43.5,50,37.4], "1860S3-7,5":[3,7.5,29,226.5,53.9,62,46.4], "1860S3-8,6":[3,8.6,37.4,292.1,69.6,80,59.9],
#                     "1860S7-6,9":[7,6.9,29,226.5,53.9,62,46.4], "1860S7-7,0":[7,7,30,234.3,55.8,64.2,48.0], "1860S7-8,0":[7,8.0,38,296.8,70.7,81.3,60.8],
#                     "1860S7-9,0":[7,9,50,390.5,93,107,80], "1860S7-9,3":[7,9.3,52,406.1,96.7,111,83.2], "1860S7-9,6":[7,9.6,55,429.6,102,117,87.7],
#                     "1860S7-11":[7,11.0,70,546.7,130,150,112], "1860S7-11,3":[7,11.3,75,585.8,140,161,120], "1860S7-12,5":[7,12.5,93,726.3,173,199,149],
#                     "1860S7-12,9":[7,12.9,100,781,186,214,160], "1860S7-13,0":[7,13,102,796.6,190,219,163], "1860S7-15,2":[7,15.2,139,1086,259,298,223],
#                     "1860S7-15,3":[7,15.3,140,1093,260,299,224], "1860S7-15,7":[7,15.7,150,1172,279,321,240]}
#
#
# strand_1920_dict = {"1920S3-6,3":[3,6.3,19.8,154.6,38,43.7,32.7],"1920S3-6,5":[3,6.5,21.2,165.6,40.7,46.8,35]}
# strand_1960_dict = {"1960S3-4,8":[3,4.8,12.0,93.7,23.5,27,20.9],"1960S3-5,2":[3,5.2,13.6,106.2,26.7,30.7,23.8], "1960S3-6,5":[3,6.5,21.2,165.5,41.6,47.8,37],
#                     "1960S3-6,85":[3,6.85,23.6,184.3,46.3,53.2,41.2], "1960S7-9,0":[7,9.0,50,390.5,98,113,86.2], "1960S7-9,3":[7,9.3,52,406.1,102,117,89.8]}
# strand_2060_dict = {"2060S3-5,2":[3,5.2,13.6,106.2,28,32.2,24.9],"2060S7-6,4":[7,6.4,25,195.3,51.5,59.2,45.3], "2060S7-6,85":[7,6.85,28.2,220.2,58.1,66.8,51.1],
#                     "2060S7-7,0":[7,7.0,30,234.3,61.8,71.1,54.4], "2060S7-8,6":[7,8.6,45,351.5,92.7,107,81.6], "2060S7-11,3":[7,11.3,75,585.8,155,178,136]}
# strand_2160_dict = {"2160S3-5,2":[3,5.2,13.6,106.2,29.4,33.8,26.2],"2160S7-6,85":[7,6.85,28.2,220.2,60.9,70,53.6]}
#
# gamma_s = 1.15
#
# rebar_dict = {"B500B":[500, 200, 0.05, 0.493]}
#
# strand_metal_name_list = list(strand_metal_dict.keys())
#
# def get_strand_metal_name_list():
#     return strand_metal_name_list
#
# def get_rebar_dict():
#     return rebar_dict
#
# strand_1770_name = list(strand_1770_dict.keys())
# strand_1860_name = list(strand_1860_dict.keys())
# strand_1920_name = list(strand_1920_dict.keys())
# strand_1960_name = list(strand_1960_dict.keys())
# strand_2060_name = list(strand_2060_dict.keys())
# strand_2160_name = list(strand_2160_dict.keys())
#
# strand_name_list = [strand_1770_name, strand_1860_name, strand_1920_name, strand_1960_name, strand_2060_name, strand_2160_name]
#
# def get_strand_name_list():
#     return strand_name_list
#
# strand_dict = {strand_metal_name_list[0]:strand_1770_dict,strand_metal_name_list[1]:strand_1860_dict,strand_metal_name_list[2]:strand_1920_dict,
#                strand_metal_name_list[3]:strand_1960_dict,strand_metal_name_list[4]:strand_2060_dict,strand_metal_name_list[5]:strand_2160_dict}
#
# def get_strand_dict():
#     return strand_dict
#
# def get_concrete_name_list():
#     return concrete_name_list
#
# def get_concrete_dict():
#     return concrete_dict
#
# length = 2400.0  # New length
#
# flange_width = 50.0
# flange_thickness = 14.0
# web_width = 16.0
# web_height = 100.0
# web_height1 = 135.0
# bottom_flange_width = 40.0
# bottom_flange_height = 30.0
#
# def get_length_effective(l, c1, c2):
#     length_eff = l - c1/100 - c2/100
#     return length_eff
#
# def get_cross_section_area_concrete(flange_width, flange_thickness, web_width, web_height, bottom_flange_width, bottom_flange_height):
#     cross_section_area_concrete = flange_width*flange_thickness + (web_height-flange_thickness-bottom_flange_height) * web_width + bottom_flange_height * bottom_flange_width
#     return cross_section_area_concrete
#
# def fig_cross_section1(flange_width, flange_thickness, web_width, web_height, bottom_flange_width, bottom_flange_height):
#
#     if web_height <= (flange_thickness + bottom_flange_height):
#         bottom_flange_height = web_height - flange_thickness
#         web_width = bottom_flange_width
#
#     y1 = [-flange_width / 2, -web_width / 2, -web_width / 2, -bottom_flange_width / 2, -bottom_flange_width / 2, bottom_flange_width / 2, bottom_flange_width / 2, web_width / 2, web_width / 2, flange_width / 2,
#           flange_width / 2, -flange_width / 2, -flange_width / 2]
#     z1 = [web_height - flange_thickness, web_height - flange_thickness, bottom_flange_height, bottom_flange_height, 0, 0, bottom_flange_height, bottom_flange_height, web_height - flange_thickness,
#           web_height - flange_thickness, web_height, web_height, web_height - flange_thickness]
#
#     p = figure(
#         title='simple line example',
#         x_axis_label='x',
#         y_axis_label='y')
#
#     p.line(y1, z1, line_width=5, line_color = "grey", line_join = "round")
#
#     p.background_fill_alpha = 0.5
#
#     return p
#
# def fig_cross_section_with_rebar(flange_width, flange_thickness, web_width, web_height, bottom_flange_width, bottom_flange_height,rebar_coordinates,bar_diameter):
#
#     if web_height <= (flange_thickness + bottom_flange_height):
#         bottom_flange_height = web_height - flange_thickness
#         web_width = bottom_flange_width
#
#     y1 = [-flange_width / 2, -web_width / 2, -web_width / 2, -bottom_flange_width / 2, -bottom_flange_width / 2, bottom_flange_width / 2, bottom_flange_width / 2, web_width / 2, web_width / 2, flange_width / 2,
#           flange_width / 2, -flange_width / 2, -flange_width / 2]
#     z1 = [web_height - flange_thickness, web_height - flange_thickness, bottom_flange_height, bottom_flange_height, 0, 0, bottom_flange_height, bottom_flange_height, web_height - flange_thickness,
#           web_height - flange_thickness, web_height, web_height, web_height - flange_thickness]
#
#     p = figure(
#         title='simple line example',
#         x_axis_label='x',
#         y_axis_label='y')
#
#     p.line(y1, z1, line_width=5, line_color = "grey", line_join = "round")
#
#     rebars_x, rebars_y = [], []
#
#     for element in rebar_coordinates:
#         rebars_x.append(element[0]), rebars_y.append(element[1])
#
#     p.scatter(rebars_x, rebars_y, size = bar_diameter/2, fill_color="black", line_color="black")
#
#     p.background_fill_alpha = 0.5
#
#     return p
#
# def get_useful_height(web_height):
#     useful_height = 0.9 * web_height
#     return useful_height
#
# def fig_beam(length, flange_width, flange_thickness, web_width, web_height, web_height1):
#
#     x1 = [0, 0, 0, 0, 0, 0, 0, 0]
#     y1 = [-flange_width / 2, -web_width / 2, -web_width / 2, web_width / 2, web_width / 2, flange_width / 2,
#          flange_width / 2, -flange_width / 2]
#     z1 = [web_height - flange_thickness, web_height - flange_thickness, 0, 0, web_height - flange_thickness,
#          web_height - flange_thickness, web_height, web_height]
#
#
#     t_beam_vertices1 = np.array([[0,-flange_width/2,web_height - flange_thickness],[0,-web_width / 2,web_height - flange_thickness],
#                                 [0, -web_width / 2, 0], [0, web_width / 2, 0],[0,web_width / 2,web_height - flange_thickness],
#                                 [0, flange_width / 2, web_height - flange_thickness], [0, flange_width / 2, web_height],
#                                 [0, -flange_width / 2, web_height]])
#
#     t_beam_edges = [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,0]]
#     t_beam_edges1 = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]]
#
#     t_beam_vertices2 = np.array([[length/2,-flange_width/2,web_height1 - flange_thickness],[length/2,-web_width / 2,web_height1 - flange_thickness],
#                                 [length/2, -web_width / 2, 0], [length/2, web_width / 2, 0],[length/2,web_width / 2,web_height1 - flange_thickness],
#                                 [length/2, flange_width / 2, web_height1 - flange_thickness], [length/2, flange_width / 2, web_height1],
#                                 [length/2, -flange_width / 2, web_height1]])
#
#     t_beam_vertices3 = np.array([[length,-flange_width/2,web_height - flange_thickness],[length,-web_width / 2,web_height - flange_thickness],
#                                 [length, -web_width / 2, 0], [length, web_width / 2, 0],[length,web_width / 2,web_height - flange_thickness],
#                                 [length, flange_width / 2, web_height - flange_thickness], [length, flange_width / 2, web_height],
#                                 [length, -flange_width / 2, web_height]])
#
#     # Create a Plotly 3D scatter plot
#     fig = go.Figure()
#
#     # Add vertices as scatter points
#     x, y, z = zip(*t_beam_vertices1)
#     fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(width=3, color='grey'), showlegend = False))
#
#     # x, y, z = zip(*t_beam_vertices2)
#     # fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(width=3, color='grey'), showlegend = False))
#
#     x, y, z = zip(*t_beam_vertices3)
#     fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(width=3, color='grey'), showlegend = False))
#
#     # Add edges as lines
#     for edge in t_beam_edges:
#         x_values = [t_beam_vertices1[edge[0]][0], t_beam_vertices1[edge[1]][0]]
#         y_values = [t_beam_vertices1[edge[0]][1], t_beam_vertices1[edge[1]][1]]
#         z_values = [t_beam_vertices1[edge[0]][2], t_beam_vertices1[edge[1]][2]]
#         fig.add_trace(go.Scatter3d(x=x_values, y=y_values, z=z_values, mode='lines', line=dict(width=3, color='grey'), showlegend = False))
#
#     # for edge in t_beam_edges:
#     #     x_values = [t_beam_vertices2[edge[0]][0], t_beam_vertices2[edge[1]][0]]
#     #     y_values = [t_beam_vertices2[edge[0]][1], t_beam_vertices2[edge[1]][1]]
#     #     z_values = [t_beam_vertices2[edge[0]][2], t_beam_vertices2[edge[1]][2]]
#     #     fig.add_trace(go.Scatter3d(x=x_values, y=y_values, z=z_values, mode='lines', line=dict(width=3, color='grey'), showlegend = False))
#
#     for edge in t_beam_edges:
#         x_values = [t_beam_vertices3[edge[0]][0], t_beam_vertices3[edge[1]][0]]
#         y_values = [t_beam_vertices3[edge[0]][1], t_beam_vertices3[edge[1]][1]]
#         z_values = [t_beam_vertices3[edge[0]][2], t_beam_vertices3[edge[1]][2]]
#         fig.add_trace(go.Scatter3d(x=x_values, y=y_values, z=z_values, mode='lines', line=dict(width=3, color='grey'), showlegend = False))
#
#     for edge in t_beam_edges1:
#         x_values = [t_beam_vertices1[edge[0]][0], t_beam_vertices2[edge[0]][0]]
#         y_values = [t_beam_vertices1[edge[0]][1], t_beam_vertices2[edge[0]][1]]
#         z_values = [t_beam_vertices1[edge[0]][2], t_beam_vertices2[edge[0]][2]]
#         fig.add_trace(go.Scatter3d(x=x_values, y=y_values, z=z_values, mode='lines', line=dict(width=3, color='grey'), showlegend = False))
#
#     for edge in t_beam_edges1:
#         x_values = [t_beam_vertices2[edge[0]][0], t_beam_vertices3[edge[0]][0]]
#         y_values = [t_beam_vertices2[edge[0]][1], t_beam_vertices3[edge[0]][1]]
#         z_values = [t_beam_vertices2[edge[0]][2], t_beam_vertices3[edge[0]][2]]
#         fig.add_trace(go.Scatter3d(x=x_values, y=y_values, z=z_values, mode='lines', line=dict(width=3, color='grey'), showlegend = False))
#     # Set layout properties
#
#     fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
#     fig.update_layout(scene=dict(aspectmode='data'))
#
#     return fig
#
# def get_xc0(d, kszi):
#     xc0 = d*kszi
#     return xc0
#
# def get_moment_0(flange_width, flange_thickness, web_width, d, xc0, fcd):
#
#     moment_0 = (((flange_width*flange_thickness)*(d-(flange_thickness/2))+((web_width*(xc0-flange_thickness))*(d-flange_thickness-(xc0-flange_thickness)/2)))*100)*fcd/math.pow(10,6)
#     #moment_0 = (flange_width*flange_thickness)*(d-(flange_thickness/2))
#     return round(moment_0, 2)
#
#
# def get_xc(MEd, b_flange, fcd, d):
#     xc = 0.01
#     step = 1
#     epsilon = 1
#
#     while MEd * 1000000 - b_flange * 10 * xc * 10 * fcd * (d - (xc / 2)) * 10 > 0:
#         diff = MEd * 1000000 - b_flange * 10 * xc * 10 * fcd * (d - (xc / 2)) * 10
#         xc += 0.0001
#         step += 1
#
#     return xc
#
# def get_xi_c(xc, d):
#     xi_c = xc /d
#     return xi_c
#
# def get_As_needed(b, xc, fcd, fyd):
#     As_needed = b * 10  * xc * 10  * fcd /fyd
#     return As_needed
#
# def get_Ast_needed_piece(As_needed, bar_diameter):
#     n = 0
#     while n * (bar_diameter/2) * (bar_diameter/2) * math.pi < As_needed:
#         n += 1
#     return n
#
# def get_Ap_needed(khi, As_needed, fyd, fpd):
#     Ap_needed = khi * As_needed * fyd / fpd
#     return  Ap_needed
#
# def get_Ap_needed_piece(Ap_needed, strand_diameter):
#     np = 0
#     while np * (strand_diameter/2) * (strand_diameter/2) * math.pi < Ap_needed:
#         np += 1
#     return np
#
# def get_delta_s(phi, dg):
#     delta_s = max(phi, dg + 5, 20)
#     return delta_s
#
# def get_delta_px(phi_p, dg):
#     delta_px = max(dg + 5, 2 * phi_p, 20)
#     return delta_px
#
# def get_delta_py(phi_p, dg):
#     delta_py = max(dg, 2 * phi_p)
#     return delta_py
#
#
# # does the needed number of rebars fit in one row?
# def is_fit_one_row(b, cover, phi_k, delta_rebar, rebar_diameter, n):
#     if b - 2 * (cover + phi_k) >= n * rebar_diameter + (n - 1) * delta_rebar:
#         return True
#     else:
#         return False
#
#
# # how many rebars fit in one row?
# def get_m_rebar(b, cover, phi_k, delta_rebar, rebar_diameter):
#     i = 0
#     while b - 2 * (cover + phi_k) >= i * rebar_diameter + (i - 1) * delta_rebar:
#         m = i
#         i += 1
#     return m
#
#
# # how many rows do the rebars fit in?
# def get_number_of_rows(b, cover, phi_k, delta_rebar, rebar_diameter, n):
#     rows = 0
#     if b - 2 * (cover + phi_k) >= n * rebar_diameter + (n - 1) * delta_rebar:
#         rows = 1
#     else:
#         i = 0
#         while b - 2 * (cover + phi_k) >= i * rebar_diameter + (i - 1) * delta_rebar:
#             m = i
#             i += 1
#
#         if n % m != 0:
#             rows = (n // m) + 1
#         else:
#             rows = n // m
#
#     return rows
#
#
# # how big is the spacing between rebars?
# def get_gap_between_rebars(n, b, cover, phi_k, delta_rebar, rebar_diameter):
#     if n > 1:
#         actual_delta = (b - 2 * (cover + phi_k) - n * rebar_diameter) / (n - 1)
#     else:
#         actual_delta = delta_rebar
#
#     return actual_delta
#
#
# # get rebar distribution
# def get_rebar_distribution(b, cover, phi_k, delta_rebar, rebar_diameter, n, delta_y):
#     bars_in_full_row = get_m_rebar(b, cover, phi_k, delta_rebar, rebar_diameter)
#
#     rows = get_number_of_rows(b, cover, phi_k, delta_rebar, rebar_diameter, n)
#
#     remaining_bars = n
#     distribution = []
#     while remaining_bars > 0:
#         for row in range(rows):
#             if remaining_bars - bars_in_full_row > 0:
#                 distribution.append(bars_in_full_row)
#                 remaining_bars -= bars_in_full_row
#             else:
#                 distribution.append(remaining_bars)
#                 remaining_bars -= remaining_bars
#     return distribution
#
#
# # get rebar coordinates
# def get_rebar_coordinates(b, cover, phi_k, rebar_diameter, n, delta_rebar, delta_y, distribution):
#     list_of_coordinates = []
#     rows = len(distribution)
#     current_row = 0
#     while current_row < rows:
#
#         for element in range(distribution[current_row]):
#
#             delta_x_rebar = get_gap_between_rebars(n=distribution[current_row], b=b, cover=cover, phi_k=phi_k,
#                                                    delta_rebar=delta_rebar,
#                                                    rebar_diameter=rebar_diameter) + rebar_diameter
#             if current_row == 0:
#                 list_of_coordinates.append((cover + phi_k + rebar_diameter / 2 + element * delta_x_rebar - b/2, (
#                         current_row * (delta_y + rebar_diameter / 2)) + cover + phi_k + rebar_diameter / 2))
#             else:
#                 list_of_coordinates.append((cover + phi_k + rebar_diameter / 2 + element * delta_x_rebar - b/2,
#                                             (current_row * (delta_y + rebar_diameter / 2)) + cover + phi_k  + rebar_diameter/2))
#
#         current_row += 1
#     return list_of_coordinates
#
# def get_d_st_alk(web_height, coordinates):
#     centeroid_st = 0
#     for char in coordinates:
#         centeroid_st += char[-1]
#     centeroid_st /= len(coordinates)
#     return web_height - centeroid_st
#
# def centroid (coordinates):
#     sum_x, sum_y = 0, 0
#     for element in coordinates:
#             sum_x += element[0]
#             sum_y += element[1]
#     return (sum_x/len(coordinates), sum_y/len(coordinates))
