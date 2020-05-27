import geopandas as gpd
import os

def from_geodataframe(df, layername):
    layer = QgsVectorLayer("Polygon?crs=epsg:4326", layername, "memory")
    layer_data = layer.dataProvider()
    layer.startEditing()

    field_list = []
    for item in df.iteritems():
        tipe = item[1].dtype
        col = item[0]
        if tipe == 'float':
            field = QgsField(col, QVariant.Double, 'double', 10, 3)
        else:
            field = QgsField(col, QVariant.String, 'String', 80)
        field_list.append(field)

    layer_data.addAttributes(field_list) # attribute list
    layer.updateFields()

    feat_list = []
    for i, row in df.iterrows():
        feat = QgsFeature()
        feat.setAttributes(list(row))
        feat.setGeometry(QgsGeometry.fromWkt(row['geometry'].to_wkt()))
        feat_list.append(feat)

    layer_data.addFeatures(feat_list) # feature list
    layer.commitChanges()
    
    return layer

oil_path = r"E:\Development\BARATA\Riset\02-oil-spill\kepri_201812_oils\kepri_20181207_oils.shp"
oil_gdf = gpd.read_file(oil_path)
oil_gdf['DATETIME-NEW'] = [i[:-11] for i in oil_gdf['DATE-TIME']]
oil_dissolve = oil_gdf.dissolve(by='DATETIME-NEW')

oil_buffer = oil_dissolve.copy()
oil_buffer.geometry = oil_buffer.geometry.centroid.buffer(0.5)

oil_name = os.path.basename(os.path.splitext(oil_path)[0])

oil_buffer_layer = from_geodataframe(oil_buffer, oil_name+'_buffer')
QgsProject.instance().addMapLayer(oil_buffer_layer)

oil_layer = QgsVectorLayer(oil_path, oil_name, 'ogr')
QgsProject.instance().addMapLayer(oil_layer)
