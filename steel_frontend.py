from pathlib import Path
import pandas as pd
import streamlit as st
import steel_backend
import plotly.graph_objects as go
from bokeh.plotting import figure
import pandas
import math
import numpy as np
from PIL import Image

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"



PAGE_TITLE = "Steel Design Assistant"

st.set_page_config(page_title=PAGE_TITLE,

                   layout="wide")

with open(css_file, 'r') as f:
    css_content = f.read()

st.markdown('''
<style>
[data-testid="collapsedControl"] {
            display: none;
        }
.katex-html {
    text-align: left;
}
</style>''',
unsafe_allow_html=True
)

chosen_language = st.sidebar.selectbox(label = "Choose a language", options = steel_backend.language_list)

tab1, tab2, tab3, tab4 = st.tabs([str(steel_backend.set_language()[chosen_language][0]), "B", "C", "D"])

with tab1:
    col1, col2, col3 = st.columns(3,gap = "medium")
    with col1:

        with st.container(border=2):
            chosen_steel_grade = st.selectbox(label = str(steel_backend.set_language()[chosen_language][1]),
                                                          options = steel_backend.steel_grade_list)
            chosen_fy = steel_backend.steel_grade_dict[chosen_steel_grade][0]

            chosen_section = st.selectbox(label = str(steel_backend.set_language()[chosen_language][2]),options = steel_backend.L_equal_name)
            chosen_element_length = st.number_input(label = str(steel_backend.set_language()[chosen_language][3]),
                                                    min_value = 0, step = 1, value = 1000)
    with col2:
        st.image(image = steel_backend.L_equal_image, use_container_width=True)

    with st.container(border=2):
        col1, col2, col3, col4, col5 = st.columns(5, gap = "small")
        with col1:
            st.latex(str(steel_backend.set_language()[chosen_language][4]))
            st.latex(str(steel_backend.set_language()[chosen_language][5]))
            st.latex(str(steel_backend.set_language()[chosen_language][6]))
            if chosen_language == "HUN":
                st.latex(r""" keresztmetszeti \thickspace terület \thickspace =""")
            else: st.latex(r""" section \thickspace area \thickspace =""")
            st.latex(str(steel_backend.set_language()[chosen_language][8]))
            if chosen_language == "HUN":
                st.latex(r""" inercia \thickspace er\H{o}s \thickspace tengely \thickspace körül \thickspace""")
            else:
                st.latex(r""" inertia \thickspace around \thickspace the \thickspace strong \thickspace axis""")
            if chosen_language == "HUN":
                st.latex(r""" inercia \thickspace gyenge \thickspace tengely \thickspace körül \thickspace""")
            else:
                st.latex(r""" inertia \thickspace around \thickspace the \thickspace gyenge \thickspace axis""")
            if chosen_language == "HUN":
                st.latex(r""" kihajlási \thickspace görbe \thickspace """)
            else:
                st.latex(r""" buckling \thickspace curve \thickspace """)
        with col2:
            st.latex(r"""\thickspace b \thickspace =""")
            st.latex(r"""\thickspace h \thickspace =""")
            st.latex(r"""\thickspace t \thickspace =""")
            st.latex(r"""\thickspace A \thickspace =""")
            st.latex(r"""\thickspace I_y \thickspace =""")
            st.latex(r"""\thickspace I_u \thickspace =""")
            st.latex(r"""\thickspace I_v \thickspace =""")
            st.latex(r"""\thickspace""")
        with col3:
            chosen_h = steel_backend.L_equal_h[steel_backend.L_equal_name.index(chosen_section)]
            st.latex(str(chosen_h) + r"""\thickspace mm""")
            chosen_b = steel_backend.L_equal_h[steel_backend.L_equal_name.index(chosen_section)]
            st.latex(str(chosen_b) + r"""\thickspace mm""")
            st.latex(str(steel_backend.L_equal_t[steel_backend.L_equal_name.index(chosen_section)]) + r"""\thickspace mm""")
            chosen_area = steel_backend.L_equal_area[steel_backend.L_equal_name.index(chosen_section)]
            st.latex(str(chosen_area) + r"""\thickspace mm^2""")
            st.latex(str(steel_backend.L_equal_inertia[steel_backend.L_equal_name.index(chosen_section)]) + r"""\thickspace cm^4""")
            st.latex(str(steel_backend.L_equal_inertia_strong[steel_backend.L_equal_name.index(chosen_section)]) + r"""\thickspace cm^4""")
            st.latex(str(steel_backend.L_equal_inertia_weak[steel_backend.L_equal_name.index(chosen_section)]) + r"""\thickspace cm^4""")
            chosen_buckling_curve = steel_backend.L_equal_curve[steel_backend.L_equal_name.index(chosen_section)]
            st.latex(str(chosen_buckling_curve))

    with st.container(border=2):
        col1, col2, col3, col4, col5 = st.columns(5, gap = "small")
        with col1:
            st.write("")
            if chosen_language == "HUN":
                st.latex(r""" befogási \thickspace tényez\H{o}""")
            else:
                st.latex(r""" buckling \thickspace coefficient \thickspace """)
            st.write("")
            if chosen_language == "HUN":
                st.latex(r""" befogási \thickspace tényez\H{o}""")
            else:
                st.latex(r""" buckling \thickspace coefficient \thickspace """)

        with col2:
            st.write("")
            st.latex(r"""\thickspace k_y \thickspace =""")
            st.write("")
            st.latex(r"""\thickspace k_z \thickspace =""")

        with col3:
            ky = st.number_input(label="ky", min_value=0.0, max_value=3.0, value=1.0, step = 0.1)
            kz = st.number_input(label="kz", min_value=0.0, max_value=3.0, value=1.0, step = 0.1)

    with st.container(border=2):
        col1, col2, col3, col4, col5 = st.columns(5, gap="small")
        with col1:
            if chosen_language == "HUN":
                st.latex(r""" kiritkus \thickspace normáler\H{o}""")
            else:
                st.latex(r""" critical \thickspace normal \thickspace force \thickspace """)
            if chosen_language == "HUN":
                st.latex(r""" kiritkus \thickspace normáler\H{o}""")
            else:
                st.latex(r""" critical \thickspace normal \thickspace force \thickspace """)
            if chosen_language == "HUN":
                st.latex(r""" kiritkus \thickspace normáler\H{o}""")
            else:
                st.latex(r""" critical \thickspace normal \thickspace force \thickspace """)
            if chosen_language == "HUN":
                st.latex(r""" karcs\'{u}s\'{a}g""")
            else:
                st.latex(r""" slenderness """)
            if chosen_language == "HUN":
                st.latex(r""" alakhiba \thickspace tényez\H{o}""")
            else:
                st.latex(r""" imperfection \thickspace factor """)
            if chosen_language == "HUN":
                st.latex(r""" segéd \thickspace mennyiség""")
            else:
                st.latex(r""" support \thickspace value """)
            if chosen_language == "HUN":
                st.latex(r""" kihajlás \thickspace csökkent\H{o} \thickspace tényez\H{o}""")
            else:
                st.latex(r""" reduction \thickspace factor """)
            if chosen_language == "HUN":
                st.latex(r""" kihajlási \thickspace ellenállás""")
            else:
                st.latex(r""" buckling \thickspace resistance """)
        with col2:
            st.latex(r"""N_{cr, v} \thickspace =""")
            st.latex(r"""N_{cr, u} \thickspace =""")
            st.latex(r"""N_{cr} \thickspace =""")
            st.latex(r"""\bar{\lambda} \thickspace =""")
            st.latex(r"""\alpha \thickspace =""")
            st.latex(r"""\Phi \thickspace =""")
            st.latex(r"""\chi \thickspace =""")
            st.latex(r"""N_{br, d} \thickspace =""")
        with col3:

            Ncr_v = steel_backend.get_Ncr(E = 210000, I = steel_backend.L_equal_inertia_weak[steel_backend.L_equal_name.index(chosen_section)] * 10000,
                                      L = chosen_element_length * ky)
            st.latex(str(round(Ncr_v/1000,2)) + r"""\thickspace kN""")
            Ncr_u = steel_backend.get_Ncr(E=210000, I=steel_backend.L_equal_inertia_strong[
                                                          steel_backend.L_equal_name.index(chosen_section)] * 10000,
                                          L=chosen_element_length * kz)
            st.latex(str(round(Ncr_u / 1000, 2)) + r"""\thickspace kN""")
            Ncr = min(Ncr_v, Ncr_u)
            st.latex(str(round(Ncr / 1000, 2)) + r"""\thickspace kN""")

            lambda_slender = steel_backend.get_lambda(A =chosen_area*100, fy = chosen_fy, Ncr = Ncr )
            st.latex(str(round(lambda_slender,3)))
            imperfection_factor = steel_backend.get_imperfection_factor(buckling_curve = chosen_buckling_curve)
            st.latex(str(imperfection_factor))
            helper_phi = steel_backend.get_helping_factor(alpha = imperfection_factor, lambda_slender = lambda_slender)
            st.latex(str(round(helper_phi,3)))
            reduction_factor_chi = steel_backend.get_reduction_factor(phi = helper_phi, lambda_slender = lambda_slender)
            st.latex(str(round(reduction_factor_chi,3)))
            Nbrd = steel_backend.get_buckling_resistance(chi = reduction_factor_chi, area = chosen_area*100, fy = chosen_fy)
            st.latex(str(round(Nbrd / 1000, 2)) + r"""\thickspace kN""")






# # Streamlit app
# chosen_language = st.radio(label="", options=beam_backend.language_list)
#
# tab1, tab2, tab3, tab4 = st.tabs([str(beam_backend.set_language()[chosen_language][0]), str(beam_backend.set_language()[chosen_language][1]),
#                                   str(beam_backend.set_language()[chosen_language][2]), str(beam_backend.set_language()[chosen_language][3])])
# #
# #
# #
# #ANYAGJELLEMZŐK
# #
# #
# #
#
#
# with tab1:
#     col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")
#     with col1:
#         chosen_concrete = st.radio(str(beam_backend.set_language()[chosen_language][4]) + " (EN 1992-1-1)", options=beam_backend.get_concrete_name_list(), index=6)
#     with col3:
#
#         st.latex(r''' ''' + str(beam_backend.set_language()[chosen_language][5]) + r'''\thickspace karakterisztikus \thickspace értéke: \enspace f_{ck} =''' +  str(beam_backend.get_concrete_dict()[chosen_concrete][0]) + '''  \enspace N/mm^2''')
#         st.latex(r''' ''' + str(beam_backend.set_language()[chosen_language][5]) + r''' \thickspace tervezési \thickspace értéke: \enspace f_{cd} =''' + str(beam_backend.get_concrete_dict()[chosen_concrete][2]) + '''  \enspace N/mm^2''')
#         st.latex(r'''húzószilárdság \thickspace tervezési \thickspace értéke: \enspace  f_{ctd} =''' + str(beam_backend.get_concrete_dict()[chosen_concrete][3]) + '''  \enspace N/mm^2''')
#         st.latex(r'''húzószilárdság \thickspace várható \thickspace értéke: \enspace f_{ctm} =''' + str(beam_backend.get_concrete_dict()[chosen_concrete][4]) + '''  \enspace N/mm^2''')
#         st.latex(r'''tapadószilárdság \thickspace tervezési \thickspace értéke: \enspace f_{bd} =''' + str(beam_backend.get_concrete_dict()[chosen_concrete][5]) + '''  \enspace N/mm^2''')
#         st.latex(r'''kúszás \thickspace átlagos \thickspace végértéke: \enspace \phi(\infty,28) =''' + str(beam_backend.get_concrete_dict()[chosen_concrete][6]))
#         st.latex(r'''rugalmassági \thickspace modulus: \enspace E_{cm} =''' + str(beam_backend.get_concrete_dict()[chosen_concrete][7]) + '''  \enspace kN/mm^2''')
#         st.latex(r'''hatásos \thickspace rugalmassági \thickspace modulus: \enspace E_{c,eff} =''' + str(beam_backend.get_concrete_dict()[chosen_concrete][8]) + '''  \enspace kN/mm^2''')
#         st.latex(r'''zsugorodás\enspace végértéke:\enspace \epsilon_{cs,\infty} =''' + str(beam_backend.get_concrete_dict()[chosen_concrete][9]) + ''' \enspace \%_{o}''')
#         st.latex(r'''h \H{o} tágulási \enspace együttható \enspace \alpha_{t} = 10^{-5} \enspace1/°C''')
#
#
#     st.write("---")
#     col1, col2, col3, col4, col5, col6 = st.columns(6, gap="medium")
#     with col1:
#         chosen_steel = st.radio("Feszítőpászma anyagminősége", options=beam_backend.get_strand_metal_name_list())
#         st.write("")
#     with col2:
#         chosen_strand = st.radio("Feszítőpászma",options=beam_backend.get_strand_name_list()[beam_backend.get_strand_metal_name_list().index(chosen_steel)])
#
#         chosen_strand_dict = beam_backend.get_strand_dict()[chosen_steel]
#
#     with col3:
#         st.latex(r'''húzószilárdság \thickspace maximuma: \enspace f_{pk} =''' + str(
#             beam_backend.get_strand_metal_dict()[chosen_steel][0]) + '''  \enspace N/mm^2''')
#         st.latex(r'''rugalmassági \thickspace modulus: \enspace E =''' + str(
#             beam_backend.get_strand_metal_dict()[chosen_steel][1]) + '''  \enspace GPa''')
#         st.latex(r'''erek \thickspace száma \thickspace a  \thickspace pászmában  \thickspace: ''' + str(chosen_strand_dict[chosen_strand][0]) + r''' \enspace eres \enspace pászma''')
#         strand_diameter = chosen_strand_dict[chosen_strand][1]
#         st.latex(r'''pászmaátmér\H{o} : \thickspace \phi_{p} = ''' + str(strand_diameter) + r''' \enspace mm''')
#         st.latex(r'''pászma \thickspace keresztmetszeti \thickspace terület : \thickspace A_{p} = ''' + str(
#             chosen_strand_dict[chosen_strand][2]) + r''' \enspace mm^2''')
#
#
#         st.latex(r'''pászma \thickspace tömege: \thickspace g_{p} = ''' + str(
#             round(chosen_strand_dict[chosen_strand][3]/1000,3)) + r''' \enspace kg/m''')
#         st.latex(r'''húzóer\H{o} \thickspace karakterisztikus \thickspace értéke: \thickspace F_{m} = ''' + str(
#             chosen_strand_dict[chosen_strand][4]) + r''' \enspace kN''')
#         st.latex(r'''húzóer\H{o} \thickspace maximums \thickspace értéke: \thickspace F_{m,max} = ''' + str(
#             chosen_strand_dict[chosen_strand][5]) + r''' \enspace kN''')
#         st.latex(
#             r'''húzóer\H{o} \thickspace 0,1\%-os \thickspace karakterisztikus \thickspace értéke: \thickspace F_{p0,1} = ''' + str(
#                 chosen_strand_dict[chosen_strand][6]) + r''' \enspace kN''')
#
#     st.write("---")
#
#     col1, col2, col3, col4, col5, col6 = st.columns(6, gap="medium")
#     with col1:
#         st.write("Betonacél anyagminősége: B60.50")
#     with col3:
#         st.latex(r'''Folyáshatár  \thickspace karakterisztikus \thickspace értéke: \thickspace f_{yk} = ''' + str(
#             round(beam_backend.rebar_dict["B500B"][0])) + r''' \enspace N/mm^2''')
#         st.latex(r'''Folyáshatár  \thickspace tervezési \thickspace értéke: \thickspace f_{yd} = ''' + str(
#             round(beam_backend.rebar_dict["B500B"][0]/beam_backend.gamma_s, 1)) + r''' \enspace N/mm^2''')
#         st.latex(r'''A  \thickspace rugalmassági \thickspace modulus: \thickspace E_{s} = ''' + str(
#             round(beam_backend.rebar_dict["B500B"][1])) + r''' \enspace GPa''')
#         st.latex(r'''A  \thickspace határnyúlás \thickspace karakterisztikus \thickspace értéke: \thickspace \epsilon_{su} = ''' + str(
#             round(beam_backend.rebar_dict["B500B"][2]*1000, 0)) + r''' \enspace \%_{o}''')
#
# #
# #
# #
# #GEOMETRIA
# #
# #
# #
#
# with tab2:
#
#     st.subheader('Geometria')
#     col1, col2, col3 = st.columns(3, gap="medium")
#     with col1:
#         length_m = st.number_input("Tartó hossza: [m]",  value = 12.0, min_value=5.0, max_value = 26.0, step=0.5)
#         length = length_m * 100
#         web_height = st.number_input("Tartó magassága: [cm]", value=100.0, min_value=50.0, max_value=150.0, step=1.0)
#
#         flange_width = st.number_input("Fejlemez szélessége: [cm]", value=40.0, min_value=beam_backend.web_width, max_value=50.0,
#                                        step=1.0)
#         flange_thickness = st.number_input("Fejlemez vastagsága: [cm]", value=14.0, min_value=10.0, max_value=30.0,
#                                            step=1.0)
#         web_width = st.number_input("Gerinc vastagsága: [cm]", value=10.0, min_value=8.0, max_value=30.0, step=1.0)
#         bottom_flange_width = st.number_input("Kivastagítás alul: [cm]", value=web_width, min_value=web_width, max_value=50.0, step=1.0)
#         bottom_flange_height = st.number_input("Kivastagítás magassága: [cm]", value=20.0, min_value=10.0, max_value=50.0, step=1.0)
#         support1 = st.number_input("Tartó felfekvése egyik végén: [cm]", value=50.0, min_value=20.0, max_value=100.0, step=0.5)
#         support2 = st.number_input("Tartó felfekvése másik végén: [cm]", value=50.0, min_value=20.0, max_value=100.0, step=0.5)
#
#     with col2:
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.bokeh_chart(
#             beam_backend.fig_cross_section1(flange_width, flange_thickness, web_width, web_height, bottom_flange_width,
#                                             bottom_flange_height), use_container_width=True)
#         st.latex(r'''keresztmetszeti \thickspace terület : \thickspace A = ''' + str(
#             beam_backend.get_cross_section_area_concrete(flange_width, flange_thickness, web_width, web_height, bottom_flange_width, bottom_flange_height)) + r''' \enspace cm^2''')
#
#     with col3:
#         st.write("")
#
#
#     st.write("---")
#     tartokozep_eltero = st.checkbox("Tartóközép eltérő")
#     tartoveg_eltero = st.checkbox("Tartóvég eltérő")
#     st.write("---")
#
#     col1, col2, col3 = st.columns(3, gap="medium")
#     with col1:
#         if tartokozep_eltero:
#             web_height1 = st.number_input("Tartó magassága középen: [cm]", min_value=web_height, max_value=200.0, step=1.0)
#             st.bokeh_chart(beam_backend.fig_cross_section1(flange_width, flange_thickness, web_width, web_height=web_height1, bottom_flange_width=bottom_flange_width, bottom_flange_height=bottom_flange_height), use_container_width=True)
#             st.latex(r'''keresztmetszeti \thickspace terület \thickspace középen:''')
#             st.latex(r'''\thickspace A_{mid} = ''' + str(
#                 beam_backend.get_cross_section_area_concrete(flange_width, flange_thickness, web_width, web_height=web_height1,
#                                                              bottom_flange_width=bottom_flange_width,
#                                                              bottom_flange_height=bottom_flange_height)) + r''' \enspace cm^2''')
#         else:
#             web_height1 = web_height
#
#
#
#     with col2:
#         if tartoveg_eltero:
#             h_fesz_veg = st.number_input("Tartófej vastagsága a gerenda végein: [cm]", min_value=flange_thickness, max_value=web_height, step=1.0)
#             h_fesz_veg_hossz = st.number_input("Tartófej kivastagítás hossza: [m]", min_value=0.2, max_value=length_m / 4, step=0.05)
#             st.bokeh_chart(beam_backend.fig_cross_section1(flange_width, flange_thickness=h_fesz_veg, web_width=web_width, web_height=web_height,
#                                                 bottom_flange_width=bottom_flange_width,
#                                                 bottom_flange_height=bottom_flange_height), use_container_width=True)
#             st.latex(r'''keresztmetszeti \thickspace terület \thickspace középen:''')
#             st.latex(r'''\thickspace A_{end} = ''' + str(
#                 beam_backend.get_cross_section_area_concrete(flange_width, flange_thickness=h_fesz_veg, web_width=web_width,
#                                                              web_height=web_height1,
#                                                              bottom_flange_width=bottom_flange_width,
#                                                              bottom_flange_height=bottom_flange_height)) + r''' \enspace cm^2''')
#
#
#         else:
#             st.write("")
#
#     with col3:
#         st.write("")
#
#
#
#     st.write("---")
#
#     col1, col2, col3 = st.columns(3, gap="medium")
#     with col1:
#
#         concrete_cover = st.number_input("Betontakarás: [mm]", value=25.0, min_value=10.0, max_value=50.0, step=5.0)
#         stirrup_diameter = st.select_slider("Kengyelátmérő: [mm]", options=beam_backend.return_bar_diameter_list(),
#                                             value=beam_backend.return_bar_diameter_list()[2])
#         bar_diameter = st.select_slider("Fővasalás átmérő: [mm]", options=beam_backend.return_bar_diameter_list(),
#                                             value=beam_backend.return_bar_diameter_list()[6])
#
#     with col2:
#         st.write("")
#         st.write("")
#         st.latex(r'''Választott \thickspace betontakarás \enspace c \thickspace = ''' + str(concrete_cover) + r'''\enspace mm ''')
#         st.write("")
#         st.write("")
#         st.latex(r'''Választott \thickspace kengyelátmér\H{o} \enspace \Phi_{k} \thickspace = ''' + str(stirrup_diameter) + r'''\enspace mm ''')
#         st.write("")
#         st.write("")
#         st.latex(r'''Választott \thickspace f\H{o}vasalásátmér\H{o} \enspace \Phi_{st} \thickspace = ''' + str(bar_diameter) + r'''\enspace mm ''')
#
#     st.plotly_chart(beam_backend.fig_beam(length, flange_width, flange_thickness, web_width, web_height, web_height1))
#
#
# #
# #
# #
# #IGÉNYBEVÉTELEK
# #
# #
# #
#
# with tab3:
#
#     col1, col2, col3 = st.columns(3, gap="medium")
#     with col1:
#         st.write("Teherbírási igénybevételek")
#         momentum_ULS = st.number_input("Nyomaték a teherbírási teherkombinációból: [kNm]", value=100.0, min_value=0.0, max_value=10000.0)
#         shear_ULS = st.number_input("Nyíróerő a teherbírási teherkombinációból: [kN]", value=100.0, min_value=0.0, max_value=10000.0)
#     with col2:
#         st.write("Kvázi-állandó igénybevételek")
#         momentum_qp = st.number_input("Nyomaték a kvázi-állandó teherkombinációból: [kNm]", value=100.0, min_value=0.0, max_value=10000.0)
#         shear_qp = st.number_input("Nyíróerő a kvázi-állandó teherkombinációból: [kN]", value=100.0, min_value=0.0, max_value=10000.0)
#     with col3:
#         st.write("Gyakori igénybevételek")
#         momentum_fr = st.number_input("Nyomaték a gyakori teherkombinációból: [kNm]", value=100.0, min_value=0.0, max_value=10000.0)
#         shear_fr = st.number_input("Nyíróerő a gyakori teherkombinációbó: [kN]", value=100.0, min_value=0.0, max_value=10000.0)
#
#     st.write("---")
#
#     dinam = {"Teherkombináció" : ["ULS", "Kvázi-állandó", "Gyakori"],"Nyomaték [kNm]": [momentum_ULS, momentum_qp, momentum_fr],
#                 "Nyíróerő [kN]": [shear_ULS, shear_qp, shear_fr]}
#
#     dinam_df = pd.DataFrame(dinam, columns = ["Teherkombináció", "Nyomaték [kNm]", "Nyíróerő [kN]"], )
#
#     st.table(data=dinam_df)
#
#
#
# #
# #
# #
# #SZÁMÍTÁS
# #
# #
# #
#
#
# with tab4:
#
#     st.subheader("Statikai váz")
#     col1, col2, col3 = st.columns(3, gap="large")
#     with col1:
#
#         st.latex(r"""Tartó \thickspace hossz:  \thickspace \thickspace \thickspace \thickspace \thickspace  """)
#         st.latex(r"""Tartó \thickspace \thickspace felfekvése\thickspace  egyik \thickspace  végén: \thickspace \thickspace \thickspace \thickspace \thickspace""")
#         st.latex(r"""Tartó \thickspace felfekvése \thickspace másik \thickspace végén:\thickspace \thickspace \thickspace \thickspace \thickspace """)
#         st.latex(r"""Effektív \thickspace tartó \thickspace hossz: \thickspace \thickspace \thickspace \thickspace \thickspace  """)
#
#     with col3:
#         st.latex(r"""L \thickspace = \thickspace""" + str(length_m) + r"""\thickspace m""")
#         st.latex(r"""c_{1} \thickspace = \thickspace""" + str(support1) + r"""\thickspace cm""")
#         st.latex(r"""c_{2} \thickspace = \thickspace""" + str(support2) + r"""\thickspace cm""")
#         st.latex(r"""L_{eff} \thickspace = \thickspace""" + str(beam_backend.get_length_effective(l=length_m, c1=support1, c2=support2)) + r"""\thickspace m""")
#
#     st.write("---")
#
#     st.subheader("A vasalás (lágyvasalás és feszítőbetétek) mennyiségének meghatározása")
#     st.latex(r'''Az \thickspace M_{Ed} \thickspace nyomaték \thickspace felvételéhez \thickspace szükséges \thickspace vasmennyiség
#     \thickspace számítása \thickspace abban \thickspace az \thickspace esetben, \thickspace ha \thickspace csak \thickspace lágyvasalást
#     \thickspace alkalmaznánk''')
#     st.latex(r'''alkalmaznánk \thickspace a \thickspace tartóban \thickspace (a  \thickspace számítás \thickspace
#      során \thickspace feltételezzük, \thickspace hogy \thickspace x_{c} \thickspace kisebb, \thickspace mint \thickspace
#       a \thickspace fejlemez \thickspace vastagsága \thickspace és \thickspace az \thickspace acélbetétek \thickspace képlékenyek)''')
#
#     col1, col2, col3 = st.columns(3, gap="large")
#
#     with col1:
#         st.latex(r"""A \thickspace hasznos \thickspace magasságot \thickspace közelít\H{o}leg \thickspace
#         az \thickspace alábbi \thickspace értékre \thickspace vesszük \thickspace fel: """)
#         st.latex(r'''Nyomatéki \thickspace igénybevétel \thickspace teherbírási \thickspace határállapotban:''')
#         st.write("")
#         st.latex(r'''Nyomatéki \thickspace egyensúlyi \thickspace egyenlet \thickspace a \thickspace húzott \thickspace
#         vasak \thickspace súlypontjára:''')
#         st.write("")
#         st.latex(r'''A \thickspace fenti \thickspace egyenletb\H{o}l \thickspace meghatározzuk \thickspace \thickspace a
#                 \thickspace nyomott \thickspace zóna \thickspace magasságát:''')
#         st.latex(r'''A \thickspace kezdeti \thickspace feltevések \thickspace ellen\H{o}rzése:''')
#         st.write("")
#
#
#     with col3:
#         st.latex(r"""d \thickspace = \thickspace""" + str(beam_backend.get_useful_height(web_height)) + r"""\thickspace cm""")
#
#         st.latex(r'''M_{Ed} \thickspace = \thickspace''' +str(momentum_ULS) + r''' kNm''')
#         st.latex(r'''M_{Ed} \thickspace = \thickspace b_{fejlemez} \thickspace \cdot \thickspace x_{c} \cdot \thickspace f_{cd} \thickspace
#          \cdot \thickspace  \left( d \thickspace - \thickspace \cfrac{x_{c}}{2} \right)''')
#         xc = beam_backend.get_xc(MEd=momentum_ULS, b_flange=flange_width, fcd=beam_backend.get_concrete_dict()[chosen_concrete][2], d=beam_backend.get_useful_height(web_height))
#         st.latex(r'''x_{c} \thickspace = \thickspace''' +str(round(xc, 2)) + r"""\thickspace cm \thickspace \textcolor{red}{(!)}""")
#
#
#
#         st.latex(r'''x_{c} \thickspace = \thickspace''' +str(round(beam_backend.get_xc(MEd=momentum_ULS, b_flange=flange_width, fcd=beam_backend.get_concrete_dict()[chosen_concrete][2], d=beam_backend.get_useful_height(web_height)), 2))
#                  + r'''\thickspace cm \thickspace \thickspace \thickspace < \thickspace \thickspace \thickspace b_{fejlemez} \thickspace = ''' + str(flange_thickness) + r'''\thickspace cm''')
#
#         if beam_backend.get_xc(MEd=momentum_ULS, b_flange=flange_width, fcd=beam_backend.get_concrete_dict()[chosen_concrete][2], d=beam_backend.get_useful_height(web_height)) <= flange_thickness:
#             st.latex(r'''A \thickspace kezdeti \thickspace feltevés \thickspace helyes \thickspace volt.''')
#         else:
#             st.latex(r'''A \thickspace kezdeti \thickspace feltevés \thickspace nem \thickspace volt \thickspace helyes.''')
#         kszi_c = beam_backend.get_xi_c(xc=beam_backend.get_xc(MEd=momentum_ULS, b_flange=flange_width, fcd=beam_backend.get_concrete_dict()[chosen_concrete][2], d=beam_backend.get_useful_height(web_height)), d=beam_backend.get_useful_height(web_height))
#         st.latex(r'''\xi_{c} \thickspace = \thickspace \cfrac{x_{c}}{d} \thickspace = \thickspace''' + str(round(kszi_c, 2)))
#         st.latex(r'''\xi_{c} \thickspace = \thickspace''' + str(round(kszi_c, 2))
#                  + r''' \thickspace \thickspace \thickspace < \thickspace \thickspace \thickspace \xi_{co} \thickspace = ''' + str(beam_backend.rebar_dict["B500B"][3]))
#         if kszi_c <= beam_backend.rebar_dict["B500B"][3]:
#             st.latex(r'''A \thickspace kezdeti \thickspace feltevés \thickspace helyes \thickspace volt.''')
#         else:
#             st.latex(
#                 r'''A \thickspace kezdeti \thickspace feltevés \thickspace nem \thickspace volt \thickspace helyes.''')
#
#
#     st.latex(r'''Az \thickspace M_{Ed} \thickspace felvételéhez \thickspace szükséges \thickspace lágyvas \thickspace mennyiség:''')
#
#     As_needed = beam_backend.get_As_needed(b=flange_width, xc=xc, fcd=beam_backend.get_concrete_dict()[chosen_concrete][2], fyd=beam_backend.rebar_dict["B500B"][0])
#
#     col1, col2, col3 = st.columns(3, gap="large")
#     with col1:
#         st.latex(r'''Az \thickspace M_{Ed} \thickspace felvételéhez \thickspace szükséges \thickspace lágyvasalás \thickspace mennyiség:''')
#
#
#     with col3:
#         st.latex(r'''A_{s.szüks} \thickspace = \cfrac{b_{fejlemez} \thickspace \cdot \thickspace x_{c} \thickspace \cdot \thickspace f_{cd}}{f_{yd}} \thickspace = \thickspace''' + str(round(As_needed, 2)) + r'''\thickspace mm^2''')
#
#     st.latex(r'''A \thickspace feszített \thickspace tartókban \thickspace rendszerint \thickspace vegyesen  \thickspace alkalmazunk
#      lágyvasalást \thickspace és \thickspace feszít\H{o}betéteket.''')
#     st.latex(r'''A \thickspace feszítés \thickspace szükséges \thickspace mértékét \thickspace els\H{o}sorban
#     gazdaságossági \thickspace alapon \thickspace dönthetjük \thickspace el.''')
#     st.latex(r'''A \thickspace tartóba \thickspace helyezett \thickspace lágyvasalás \thickspace (A_{st}) \thickspace és \thickspace
#     feszít\H{o}betétek \thickspace (A_{p}) \thickspace mennyiségének \thickspace arányát \thickspace az \thickspace ún. \thickspace
#     feszítési \thickspace fokkal \thickspace írhatjuk \thickspace le:''')
#     st.latex(r''' \chi \thickspace =
#     \thickspace \cfrac{A_{p} \thickspace \cdot \thickspace f_{pd}}
#     { A_{p} \thickspace \cdot \thickspace f_{pd} \thickspace + \thickspace A_{st} \thickspace \cdot \thickspace f_{yd}}''')
#     st.latex(r'''Magasépítési \thickspace szerkezeteknél \thickspace általában \thickspace a \thickspace \chi \thickspace =
#     \thickspace 0,7...0,8 \thickspace körüli \thickspace érték \thickspace alkalmazása \thickspace eredményezi \thickspace
#     a \thickspace leggazdaságosabb \thickspace megoldást.''')
#
#     col1, col2, col3 = st.columns(3, gap="large")
#     with col1:
#         st.write("")
#         st.latex(
#             r'''Feszítési \thickspace fok: \thickspace ''')
#     with col2:
#         khi = st.slider(label="", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
#
#     with col3:
#         st.write("")
#         st.latex(r'''\chi \thickspace =''' + str(khi))
#
#     st.latex(r'''Ez \thickspace alapján \thickspace a \thickspace szükséges \thickspace lágyvasalás \thickspace
#     és \thickspace feszít\H{o}betét \thickspace mennyiségek:''')
#
#     col1, col2, col3 = st.columns(3, gap="large")
#     with col1:
#         st.latex(r'''A_{st.szüks} \thickspace = \thickspace \left( 1 \thickspace - \thickspace \chi \right)
#         \thickspace \cdot \thickspace A_{s.szüks}''')
#         st.latex(r'''Alkalmazott \thickspace lágyvasalás \thickspace átmér\H{o}:''')
#         st.latex(r'''Szükséges \thickspace lágyvasalás \thickspace darabszám:''')
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.latex(r'''Alkalmazott \thickspace lágyvasalás \thickspace darabszám:''')
#         st.latex(r'''Alkalmazott \thickspace lágyvasalás:''')
#         st.latex(r'''A_{p.szüks} \thickspace = \thickspace \chi \cdot \thickspace A_{s.szüks} \cfrac{f_{yd}}{f_{pd}}''')
#         st.latex(r'''Alkalmazott \thickspace pászmaátmér\H{o}:''')
#         st.latex(r'''Szükséges \thickspace pászma \thickspace darabszám:''')
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.write("")
#         st.latex(r'''Alkalmazott \thickspace pászma \thickspace darabszám:''')
#         st.latex(r'''Alkalmazott \thickspace pászma \thickspace terület:''')
#
#     Ast_szuks = (1-khi) * As_needed
#     with col3:
#         st.latex(r'''A_{st.szüks} \thickspace = ''' + str(round(Ast_szuks, 2)) + r'''\thickspace mm^2''')
#         st.latex(r'''\phi_{st} \thickspace =''' + str(bar_diameter) + r'''\thickspace mm''')
#         n_needed = beam_backend.get_Ast_needed_piece(As_needed=Ast_szuks,bar_diameter=bar_diameter)
#         st.latex(r'''n_{st.szüks} \thickspace =''' + str(n_needed))
#         n_alk = st.slider(label="", min_value=2, max_value=30, value=n_needed, step=1)
#         st.latex(r'''n_{st.alk} \thickspace =''' + str(n_alk))
#         Ast_alk = n_alk * (bar_diameter/2) * (bar_diameter/2) * math.pi
#         st.latex(r'''A_{st.alk} \thickspace = ''' + str(round(Ast_alk, 2)) + r'''\thickspace mm^2''')
#         Ap_needed = beam_backend.get_Ap_needed(khi=khi, As_needed=As_needed, fyd=beam_backend.rebar_dict["B500B"][0]/beam_backend.gamma_s,
#                                   fpd=beam_backend.get_strand_metal_dict()[chosen_steel][0]/beam_backend.gamma_s)
#         st.write("")
#         st.latex(r'''A_{p.szüks} \thickspace = ''' + str(round(Ap_needed, 2)) + r'''\thickspace mm^2''')
#         st.latex(r'''\phi_{p} \thickspace =''' + str(strand_diameter) + r'''\thickspace mm''')
#         np_needed = beam_backend.get_Ap_needed_piece(Ap_needed=Ap_needed, strand_diameter=chosen_strand_dict[chosen_strand][1])
#         st.latex(r'''n_{p.szüks} \thickspace =''' + str(np_needed))
#         np_alk = st.slider(label="", min_value=0, max_value=30, value=np_needed, step=1)
#         st.latex(r'''n_{p.alk} \thickspace =''' + str(np_alk))
#         Ap_alk = np_alk * (strand_diameter / 2) * (strand_diameter / 2) * math.pi
#         st.latex(r'''A_{p.alk} \thickspace = ''' + str(round(Ap_alk, 2)) + r'''\thickspace mm^2''')
#
#     st.write("---")
#     st.subheader("A keresztmetszet vasalása")
#
#     col1, col2, col3 = st.columns(3, gap="large")
#     with col1:
#         st.latex(r'''Alkalmazott \thickspace betonfedés:''')
#     with col3:
#         st.latex(str(concrete_cover) + r'''\enspace mm ''')
#
#     st.latex(r'''Az \thickspace acélbetétek \thickspace illetve \thickspace feszít\H{o}pászmák \thickspace
#     közötti \thickspace minimális \thickspace távolságok \thickspace számítása''')
#
#     col1, col2, col3 = st.columns(3, gap="large")
#     with col1:
#         st.latex(r'''Az \thickspace adalékanyag \thickspace maximális \thickspace szemátmér\H{o}je:''')
#         st.latex(r'''Lágyvasak \thickspace közötti \thickspace minimális \thickspace távolság: \thickspace \Delta_{s} =
#          \thickspace max \left( \phi_{st}, \thickspace d_{g} \thickspace + \thickspace 5 \thickspace mm, \thickspace 20
#           \thickspace mm \right)''')
#         st.latex(r'''Pászmák \thickspace \thickspace közötti \thickspace min. \thickspace vízszintes \thickspace
#         távolság: \thickspace \Delta_{px} = max \left( d_{g} \thickspace + \thickspace 5
#         \thickspace mm, \thickspace 2 \cdot \phi_{p}, \thickspace 20
#           \thickspace mm \right)''')
#         st.latex(r'''Pászmák \thickspace \thickspace közötti \thickspace min. \thickspace függ\H{o}leges \thickspace
#                 távolság: \thickspace \Delta_{py} = max \left( d_{g} \thickspace , \thickspace 2 \cdot \phi_{p} \right)''')
#     with col3:
#         dg = 16
#         st.latex(r'''d_{g} \thickspace = \thickspace''' + str(dg) + r'''\enspace mm ''')
#         delta_s = beam_backend.get_delta_s(phi = bar_diameter, dg=dg)
#         st.latex(r'''\Delta_{s} = \thickspace''' +  str(delta_s) + r'''\enspace mm ''')
#         delta_px = beam_backend.get_delta_px(phi_p = strand_diameter, dg=dg)
#         st.latex(r'''\Delta_{px} = \thickspace''' + str(delta_px) + r'''\enspace mm ''')
#         delta_py = beam_backend.get_delta_py(phi_p = strand_diameter, dg=dg)
#         st.latex(r'''\Delta_{py} = \thickspace''' + str(delta_py) + r'''\enspace mm ''')
#
#     col1, col2 = st.columns(2, gap="small")
#     with col1:
#       st.image(image = ast_ap_picture, use_column_width = "auto")
#
#     st.latex(r"""Az \thickspace alkalmazott \thickspace vasmennyiségek \thickspace és \thickspace hasznos \thickspace
#     magasságok""")
#
#
#     rebar_distribution = beam_backend.get_rebar_distribution(b=bottom_flange_width, cover=concrete_cover/10,
#                                                              phi_k=stirrup_diameter/10, delta_rebar=delta_s/10,
#                                                              rebar_diameter=bar_diameter/10, n=n_alk, delta_y=delta_s/10)
#
#     if rebar_distribution[-1] == 1:
#         st.latex(r"""\textcolor{red}{Szerkesztési \thickspace szabályok \thickspace miatt \thickspace érdemes \thickspace
#          megnövelni \thickspace az \thickspace alkalmazott \thickspace betonacélok \thickspace számát!}""")
#
#
#     rebar_coordinates = beam_backend.get_rebar_coordinates(b=bottom_flange_width, cover=concrete_cover/10, phi_k=stirrup_diameter/10,
#                                               rebar_diameter=bar_diameter/10, n=n_alk, delta_rebar=delta_s/10,
#                                                            delta_y=delta_s/10, distribution=rebar_distribution)
#     d_st_alk = beam_backend.get_d_st_alk(web_height=web_height, coordinates=rebar_coordinates)
#
#     st.latex(str(rebar_coordinates))
#
#     col1, col2, col3 = st.columns(3, gap="small")
#     with col1:
#         st.bokeh_chart(
#             beam_backend.fig_cross_section_with_rebar(flange_width, flange_thickness, web_width, web_height, bottom_flange_width,
#                                             bottom_flange_height, rebar_coordinates, bar_diameter), use_container_width=True)
#     with col2:
#         st.latex(r'''Alkalmazott \thickspace lágyvasalás \thickspace darabszám:''')
#         st.latex(r'''Alkalmazott \thickspace lágyvasalás:''')
#         st.latex(r'''Lágyvasalás \thickspace hasznos \thickspace magassága:''')
#     with col3:
#         st.latex(r'''n_{st.alk} \thickspace =''' + str(n_alk))
#         st.latex(r'''A_{st.alk} \thickspace = ''' + str(round(Ast_alk, 2)) + r'''\thickspace mm^2''')
#         st.latex(r'''n_{st.alk} \thickspace =''' + str(round(d_st_alk,2)) + r'''\thickspace cm''')
