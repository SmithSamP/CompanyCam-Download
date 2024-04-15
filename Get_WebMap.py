from arcgis.gis import GIS
from arcgis.features import FeatureLayer

gis = GIS(username="smiths_aks", password="AKS_gis2!")


# Find web map and layer
webmap_item = gis.content.search("title:6799_Photos", item_type="Web Map", outside_org=False)[0]
webmap_data = webmap_item.get_data()

# feature_layer_item = [layer['layerObject'] for layer in webmap_data['operationalLayers'] if layer['title'] == "My Feature Layer"][0]

# # Prepare updates
# updates = [
#     {'attributes': {'ObjectID': 1, 'Field1': 'New Value'}},
# ]
print(webmap_item.title)
# # Update and save
# feature_layer = FeatureLayer(feature_layer_item['url'], gis)
# feature_layer.edit_features(updates=updates)
# webmap_item.update(item_properties={'text': webmap_data})
