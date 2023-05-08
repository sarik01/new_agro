import  json


from models import Plan, Shablon_Arrange

# with open('ekin.geojson', 'r', encoding='utf-8') as f:
#     text = json.load(f)
#     # print(text)
#     for i in text['features']:
#         print(i['properties']['globalid'])
#         plan = Plan(
#             geometry=i['geometry'], globalid=i['properties']['globalid'], region=i['properties']['region'],
#             district=i['properties']['district'], crop_name=i['properties']['crop_name'],
#             crop_area=i['properties']['crop_area'], kontur_raqami=i['properties']['kontur_raqami'],
#             massiv=i['properties']['Massiv'], shape_length=i['properties']['Shape_Length'],
#             shape_area=i['properties']['Shape_Area'],
#         )
#         db.session.add(plan)
#         db.session.commit()
#     print('done')
        # geometyry json
        # globalid
        # region
        # diatrict
        # crop_name
        # crop_name

        # crop_area
        # kontur_raqami
        # Massiv
        # Shape_Length
        # Shape_Area

with open('../Shablon_Arrange.json', 'w', encoding='utf-8') as f:

    shablon = Shablon_Arrange.query.all()

    f.write(json.dumps([x for x in shablon]))