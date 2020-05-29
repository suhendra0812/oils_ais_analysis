<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyMaxScale="1" simplifyDrawingTol="1" styleCategories="AllStyleCategories" readOnly="0" version="3.8.2-Zanzibar" maxScale="0" simplifyAlgorithm="0" simplifyLocal="1" minScale="1e+08" hasScaleBasedVisibilityFlag="0" labelsEnabled="0" simplifyDrawingHints="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" forceraster="0" enableorderby="0" type="categorizedSymbol" attr="NEGARA">
    <categories>
      <category value="INDONESIA" render="true" label="Wilayah Indonesia" symbol="0"/>
      <category value="" render="true" label="Bukan Wilayah Indonesia" symbol="1"/>
    </categories>
    <symbols>
      <symbol force_rhr="0" type="fill" alpha="1" clip_to_extent="1" name="0">
        <layer locked="0" pass="0" class="SimpleFill" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="177,177,177,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
      <symbol force_rhr="0" type="fill" alpha="1" clip_to_extent="1" name="1">
        <layer locked="0" pass="0" class="SimpleFill" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="255,255,255,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <source-symbol>
      <symbol force_rhr="0" type="fill" alpha="1" clip_to_extent="1" name="0">
        <layer locked="0" pass="0" class="SimpleFill" enabled="1">
          <prop v="3x:0,0,0,0,0,0" k="border_width_map_unit_scale"/>
          <prop v="67,162,148,255" k="color"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0.26" k="outline_width"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="solid" k="style"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option name="properties"/>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </source-symbol>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions">
      <value>REGION</value>
    </property>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory minScaleDenominator="0" scaleDependency="Area" rotationOffset="270" labelPlacementMethod="XHeight" lineSizeType="MM" sizeScale="3x:0,0,0,0,0,0" backgroundAlpha="255" lineSizeScale="3x:0,0,0,0,0,0" minimumSize="0" width="15" maxScaleDenominator="1e+08" height="15" backgroundColor="#ffffff" sizeType="MM" diagramOrientation="Up" enabled="0" opacity="1" barWidth="5" penAlpha="255" penColor="#000000" penWidth="0" scaleBasedVisibility="0">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <attribute label="" field="" color="#000000"/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" obstacle="0" dist="0" priority="0" zIndex="0" placement="1" showAll="1">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="REGION">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="PROVINSI">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="NEGARA">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="REGION" name=""/>
    <alias index="1" field="PROVINSI" name=""/>
    <alias index="2" field="NEGARA" name=""/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default expression="" applyOnUpdate="0" field="REGION"/>
    <default expression="" applyOnUpdate="0" field="PROVINSI"/>
    <default expression="" applyOnUpdate="0" field="NEGARA"/>
  </defaults>
  <constraints>
    <constraint unique_strength="0" field="REGION" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="PROVINSI" exp_strength="0" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" field="NEGARA" exp_strength="0" notnull_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="REGION" desc=""/>
    <constraint exp="" field="PROVINSI" desc=""/>
    <constraint exp="" field="NEGARA" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortExpression="&quot;WILAYAH&quot;" actionWidgetStyle="dropDown" sortOrder="1">
    <columns>
      <column width="-1" type="actions" hidden="1"/>
      <column width="-1" type="field" hidden="0" name="REGION"/>
      <column width="-1" type="field" hidden="0" name="PROVINSI"/>
      <column width="-1" type="field" hidden="0" name="NEGARA"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>generatedlayout</editorlayout>
  <editable>
    <field editable="1" name="IBU_KABU"/>
    <field editable="1" name="IBU_PROV"/>
    <field editable="1" name="KABUPATEN"/>
    <field editable="1" name="KODE_BPS"/>
    <field editable="1" name="KODE_UNSUR"/>
    <field editable="1" name="LUAS_KABU"/>
    <field editable="1" name="LUAS_PROV"/>
    <field editable="1" name="LUAS_UNSUR"/>
    <field editable="1" name="NAMA_UNSUR"/>
    <field editable="1" name="NEGARA"/>
    <field editable="1" name="POPU_KABU"/>
    <field editable="1" name="POPU_PROV"/>
    <field editable="1" name="PROVINSI"/>
    <field editable="1" name="REGION"/>
    <field editable="1" name="TOPONYM"/>
    <field editable="1" name="WEB_KABU"/>
    <field editable="1" name="WEB_PROV"/>
    <field editable="1" name="WILAYAH"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="IBU_KABU"/>
    <field labelOnTop="0" name="IBU_PROV"/>
    <field labelOnTop="0" name="KABUPATEN"/>
    <field labelOnTop="0" name="KODE_BPS"/>
    <field labelOnTop="0" name="KODE_UNSUR"/>
    <field labelOnTop="0" name="LUAS_KABU"/>
    <field labelOnTop="0" name="LUAS_PROV"/>
    <field labelOnTop="0" name="LUAS_UNSUR"/>
    <field labelOnTop="0" name="NAMA_UNSUR"/>
    <field labelOnTop="0" name="NEGARA"/>
    <field labelOnTop="0" name="POPU_KABU"/>
    <field labelOnTop="0" name="POPU_PROV"/>
    <field labelOnTop="0" name="PROVINSI"/>
    <field labelOnTop="0" name="REGION"/>
    <field labelOnTop="0" name="TOPONYM"/>
    <field labelOnTop="0" name="WEB_KABU"/>
    <field labelOnTop="0" name="WEB_PROV"/>
    <field labelOnTop="0" name="WILAYAH"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>REGION</previewExpression>
  <mapTip>FID_</mapTip>
  <layerGeometryType>2</layerGeometryType>
</qgis>
