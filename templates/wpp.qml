<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" labelsEnabled="0" version="3.4.4-Madeira" minScale="1e+08" simplifyAlgorithm="0" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" maxScale="0" simplifyDrawingTol="1" simplifyDrawingHints="1" readOnly="0" simplifyLocal="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" enableorderby="0" symbollevels="0" forceraster="0">
    <symbols>
      <symbol alpha="1" name="0" type="line" force_rhr="0" clip_to_extent="1">
        <layer enabled="1" locked="0" pass="1" class="SimpleLine">
          <prop v="square" k="capstyle"/>
          <prop v="3;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="1,43,255,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.36" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="1" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory backgroundAlpha="255" lineSizeType="MM" scaleDependency="Area" backgroundColor="#ffffff" penColor="#000000" rotationOffset="270" opacity="1" labelPlacementMethod="XHeight" sizeScale="3x:0,0,0,0,0,0" diagramOrientation="Up" sizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" penWidth="0" maxScaleDenominator="1e+08" width="15" scaleBasedVisibility="0" minimumSize="0" enabled="0" height="15" minScaleDenominator="0" barWidth="5" penAlpha="255">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings placement="2" linePlacementFlags="18" showAll="1" dist="0" obstacle="0" priority="0" zIndex="0">
    <properties>
      <Option type="Map">
        <Option name="name" type="QString" value=""/>
        <Option name="properties"/>
        <Option name="type" type="QString" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <fieldConfiguration>
    <field name="OBJECTID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="LEFT_FID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="RIGHT_FID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="Shape_Leng">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="OBJECTID" index="0"/>
    <alias name="" field="LEFT_FID" index="1"/>
    <alias name="" field="RIGHT_FID" index="2"/>
    <alias name="" field="Shape_Leng" index="3"/>
  </aliases>
  <excludeAttributesWMS/>
  <excludeAttributesWFS/>
  <defaults>
    <default field="OBJECTID" applyOnUpdate="0" expression=""/>
    <default field="LEFT_FID" applyOnUpdate="0" expression=""/>
    <default field="RIGHT_FID" applyOnUpdate="0" expression=""/>
    <default field="Shape_Leng" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint field="OBJECTID" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="LEFT_FID" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="RIGHT_FID" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
    <constraint field="Shape_Leng" constraints="0" unique_strength="0" notnull_strength="0" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="OBJECTID"/>
    <constraint exp="" desc="" field="LEFT_FID"/>
    <constraint exp="" desc="" field="RIGHT_FID"/>
    <constraint exp="" desc="" field="Shape_Leng"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column type="actions" hidden="1" width="-1"/>
      <column name="OBJECTID" type="field" hidden="0" width="-1"/>
      <column name="LEFT_FID" type="field" hidden="0" width="-1"/>
      <column name="RIGHT_FID" type="field" hidden="0" width="-1"/>
      <column name="Shape_Leng" type="field" hidden="0" width="-1"/>
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
    <field name="Id" editable="1"/>
    <field name="LEFT_FID" editable="1"/>
    <field name="OBJECTID" editable="1"/>
    <field name="RIGHT_FID" editable="1"/>
    <field name="Shape_Leng" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="Id" labelOnTop="0"/>
    <field name="LEFT_FID" labelOnTop="0"/>
    <field name="OBJECTID" labelOnTop="0"/>
    <field name="RIGHT_FID" labelOnTop="0"/>
    <field name="Shape_Leng" labelOnTop="0"/>
  </labelOnTop>
  <widgets/>
  <previewExpression>Id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
