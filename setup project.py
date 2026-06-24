"""
RetailMap SF — QGIS Portfolio Project Setup
============================================
Run this script inside the QGIS Python Console to automatically build
a complete, styled GIS project from stores.geojson, including:

  ✓  OpenStreetMap basemap (XYZ tiles)
  ✓  Categorized point layer  (6 store categories, custom colors)
  ✓  Rating-weighted heatmap layer  (toggle on/off)
  ✓  Store name labels  (visible at 1:50 000 and closer)
  ✓  Professional A4 print layout  (title, map, legend, scale bar)
  ✓  Auto-save as  retailmap_sf.qgs

HOW TO RUN
──────────
  1.  Open QGIS Desktop  (3.16 or newer)
  2.  Plugins  →  Python Console  (Ctrl + Alt + P)
  3.  Click the  "Show Editor"  button  (📄 icon, top-right of console)
  4.  Click  "Open Script…"  and choose this file
           — OR paste everything below the dashed line —
  5.  Click the green  ▶ Run  button
  6.  retailmap_sf.qgs  is created in the same folder as stores.geojson

REQUIREMENTS
────────────
  • QGIS 3.16+ (LTS recommended)
  • stores.geojson  in the same folder as this script
  • Internet connection  (for the OSM basemap tile layer)
"""

import os
from qgis.core import (
    Qgis,
    QgsProject,
    QgsVectorLayer, QgsRasterLayer,
    QgsCoordinateReferenceSystem, QgsRectangle,
    QgsCategorizedSymbolRenderer, QgsRendererCategory, QgsMarkerSymbol,
    QgsHeatmapRenderer, QgsGradientColorRamp, QgsGradientStop,
    QgsPalLayerSettings, QgsVectorLayerSimpleLabeling,
    QgsTextFormat, QgsTextBufferSettings,
    QgsPrintLayout, QgsLayoutItemMap, QgsLayoutItemLegend,
    QgsLayoutItemLabel, QgsLayoutItemScaleBar, QgsLayoutItemPage,
    QgsLayoutSize, QgsUnitTypes,
)
from qgis.PyQt.QtGui  import QColor, QFont
from qgis.PyQt.QtCore import QRectF

print('\n' + '─'*52)
print('  RetailMap SF  —  QGIS Project Setup')
print('─'*52)

# ─────────────────────────────────────────────────────────
# 0.  Locate stores.geojson
# ─────────────────────────────────────────────────────────
script_dir = (
    os.path.dirname(os.path.abspath(__file__))
    if '__file__' in dir()
    else os.path.dirname(QgsProject.instance().fileName()) or os.path.expanduser('~')
)
geojson_path = os.path.join(script_dir, 'stores.geojson')

if not os.path.exists(geojson_path):
    from qgis.PyQt.QtWidgets import QFileDialog
    geojson_path, _ = QFileDialog.getOpenFileName(
        None, 'Select stores.geojson', script_dir,
        'GeoJSON Files (*.geojson *.json)')

if not os.path.exists(geojson_path):
    raise FileNotFoundError(
        '\n  stores.geojson not found.\n'
        f'  Expected: {script_dir}\n'
        '  Place stores.geojson in the same folder as this script and re-run.')

print(f'  Data  : {geojson_path}')

# ─────────────────────────────────────────────────────────
# 1.  Project settings
# ─────────────────────────────────────────────────────────
project = QgsProject.instance()
project.setTitle('RetailMap SF — Store Intelligence')
project.setCrs(QgsCoordinateReferenceSystem('EPSG:4326'))
project.setBackgroundColor(QColor('#f0f0f0'))

# ─────────────────────────────────────────────────────────
# 2.  Category colour palette
# ─────────────────────────────────────────────────────────
#  name           fill       outline
PALETTE = {
    'Grocery':     ('#4ECDC4', '#279E96'),
    'Electronics': ('#FF6B35', '#CC4A0F'),
    'Fashion':     ('#B57BFF', '#8A4ECC'),
    'Pharmacy':    ('#2DCC85', '#1A9960'),
    'Sports':      ('#FFC947', '#CC9600'),
    'Home':        ('#FF6B9D', '#CC3870'),
}

# ─────────────────────────────────────────────────────────
# 3.  OpenStreetMap basemap  (XYZ tile layer)
# ─────────────────────────────────────────────────────────
osm_uri = ('type=xyz'
           '&url=https://tile.openstreetmap.org/{z}/{x}/{y}.png'
           '&zmax=19&zmin=0'
           '&crs=EPSG4326')
osm = QgsRasterLayer(osm_uri, 'OpenStreetMap', 'wms')
if osm.isValid():
    project.addMapLayer(osm)
    print('  [✓] OSM basemap added')
else:
    print('  [!] OSM tile layer could not be validated — it will still')
    print('      render at runtime when an internet connection is available.')
    project.addMapLayer(osm)

# ─────────────────────────────────────────────────────────
# 4.  Load GeoJSON vector layer
# ─────────────────────────────────────────────────────────
stores = QgsVectorLayer(geojson_path, 'SF Retail Stores', 'ogr')
if not stores.isValid():
    raise RuntimeError(f'  Failed to load GeoJSON:\n  {geojson_path}')
print(f'  [✓] {stores.featureCount()} stores loaded')

# ─────────────────────────────────────────────────────────
# 5.  Rating-weighted heatmap layer  (same data source)
# ─────────────────────────────────────────────────────────
heat = QgsVectorLayer(geojson_path, 'Store Density Heatmap', 'ogr')
if heat.isValid():
    hr = QgsHeatmapRenderer()
    hr.setRadius(15.0)
    hr.setRadiusUnit(QgsUnitTypes.RenderPixels)
    hr.setWeightExpression('"rating"')   # higher-rated stores glow brighter
    hr.setMaximumValue(0)                # 0 = auto-scale

    # Colour ramp: transparent → teal → yellow → orange
    ramp = QgsGradientColorRamp(
        QColor(240, 240, 240,   0),   # transparent  (cold / sparse)
        QColor(255,  90,  53, 230),   # orange        (hot  / dense)
    )
    ramp.setStops([
        QgsGradientStop(0.30, QColor( 78, 205, 196, 100)),  # teal
        QgsGradientStop(0.60, QColor(255, 209, 102, 190)),  # yellow
    ])
    hr.setColorRamp(ramp)
    heat.setRenderer(hr)
    heat.setOpacity(0.80)
    project.addMapLayer(heat)
    # Hide via the layer-tree node (correct API in all QGIS 3.x versions)
    root      = QgsProject.instance().layerTreeRoot()
    heat_node = root.findLayer(heat.id())
    if heat_node:
        heat_node.setItemVisibilityChecked(False)
    print('  [✓] Heatmap layer added  (hidden by default — toggle in Layers panel)')

# ─────────────────────────────────────────────────────────
# 6.  Categorized symbol renderer  (circles by category)
# ─────────────────────────────────────────────────────────
categories = []
for cat_name, (fill, outline) in PALETTE.items():
    sym = QgsMarkerSymbol.createSimple({
        'name':          'circle',
        'color':          fill,
        'outline_color':  outline,
        'outline_width': '0.5',
        'size':          '3.8',
    })
    categories.append(QgsRendererCategory(cat_name, sym, cat_name))

renderer = QgsCategorizedSymbolRenderer('category', categories)
stores.setRenderer(renderer)
print('  [✓] Categorized renderer applied')

# ─────────────────────────────────────────────────────────
# 7.  Store name labels
#     (auto-displayed when zoom ≤ 1:50 000)
# ─────────────────────────────────────────────────────────
tf = QgsTextFormat()
tf.setFont(QFont('Arial', 7, QFont.Normal))
tf.setSize(7.0)
tf.setColor(QColor('#222244'))

buf = QgsTextBufferSettings()
buf.setEnabled(True)
buf.setSize(0.8)
buf.setColor(QColor(255, 255, 255, 210))
tf.setBuffer(buf)

ls = QgsPalLayerSettings()
ls.setFormat(tf)
ls.fieldName = 'name'
# Placement enum moved to Qgis namespace in QGIS 3.30+
try:
    ls.placement = Qgis.LabelPlacement.OverPoint     # QGIS 3.30+
except AttributeError:
    ls.placement = QgsPalLayerSettings.OverPoint     # QGIS < 3.30
ls.yOffset = 3.5
ls.enabled         = True
ls.scaleVisibility = True
ls.minimumScale    = 50000    # only render labels at 1:50 000 or closer

stores.setLabeling(QgsVectorLayerSimpleLabeling(ls))
stores.setLabelsEnabled(True)
print('  [✓] Labels configured  (visible at 1:50 000 or closer)')

# ─────────────────────────────────────────────────────────
# 8.  Add stores layer and set canvas extent
# ─────────────────────────────────────────────────────────
project.addMapLayer(stores)
sf_bbox = QgsRectangle(-122.530, 37.695, -122.355, 37.835)

try:
    canvas = iface.mapCanvas()
    canvas.setExtent(sf_bbox)
    canvas.refresh()
    print('  [✓] Map canvas zoomed to San Francisco')
except NameError:
    print('  [!] iface not available — open project to set canvas manually')

# ─────────────────────────────────────────────────────────
# 9.  Print layout  (A4 landscape)
# ─────────────────────────────────────────────────────────
lm     = project.layoutManager()
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName('RetailMap SF — Print Layout')

# Page
page = QgsLayoutItemPage(layout)
try:
    page.setPageSize(QgsLayoutSize(297, 210, QgsUnitTypes.LayoutMillimeters))
except Exception:
    page.setPageSize('A4', QgsLayoutItemPage.Landscape)
layout.pageCollection().addPage(page)

# ── Map frame ──
map_item = QgsLayoutItemMap(layout)
map_item.setFrameEnabled(True)
layout.addLayoutItem(map_item)
map_item.attemptSetSceneRect(QRectF(10, 22, 195, 163))
map_item.setExtent(sf_bbox)

# ── Title ──
title = QgsLayoutItemLabel(layout)
title.setText('RetailMap SF — San Francisco Retail Intelligence')
title.setFont(QFont('Arial', 14, QFont.Bold))
title.setFontColor(QColor('#0D0F1C'))
layout.addLayoutItem(title)
title.attemptSetSceneRect(QRectF(10, 4, 200, 11))

# ── Subtitle ──
sub = QgsLayoutItemLabel(layout)
sub.setText('43 stores  ·  6 categories  ·  14 neighborhoods  ·  San Francisco, CA  ·  2024')
sub.setFont(QFont('Arial', 8))
sub.setFontColor(QColor('#4A5070'))
layout.addLayoutItem(sub)
sub.attemptSetSceneRect(QRectF(10, 14, 200, 7))

# ── Legend ──
legend = QgsLayoutItemLegend(layout)
legend.setLinkedMap(map_item)
legend.setTitle('Store Category')
legend.setAutoUpdateModel(True)
try:
    legend.setFont(QFont('Arial', 9))
except AttributeError:
    pass   # font API differs across QGIS versions — legend will use defaults
layout.addLayoutItem(legend)
legend.attemptSetSceneRect(QRectF(210, 22, 82, 75))

# ── Scale bar ──
sbar = QgsLayoutItemScaleBar(layout)
sbar.setLinkedMap(map_item)
sbar.applyDefaultSize()
try:
    sbar.setFont(QFont('Arial', 7))
except AttributeError:
    pass
layout.addLayoutItem(sbar)
sbar.attemptSetSceneRect(QRectF(10, 188, 80, 8))

# ── Data note ──
note = QgsLayoutItemLabel(layout)
note.setText('Note: Store data is simulated for portfolio/educational purposes.')
note.setFont(QFont('Arial', 6))
note.setFontColor(QColor('#9CA3AF'))
layout.addLayoutItem(note)
note.attemptSetSceneRect(QRectF(100, 189, 140, 5))

lm.addLayout(layout)
print('  [✓] Print layout created: "RetailMap SF — Print Layout"')

# ─────────────────────────────────────────────────────────
# 10.  Save project
# ─────────────────────────────────────────────────────────
save_path = os.path.join(os.path.dirname(geojson_path), 'retailmap_sf.qgs')
project.write(save_path)

print()
print('─'*52)
print('  ✅  Done!  Project saved:')
print(f'      {save_path}')
print('─'*52)
print('  NEXT STEPS ')
print('  ──────────')
print('  • Open retailmap_sf.qgs in QGIS to view your project')
print('  • Toggle "Store Density Heatmap" layer in the Layers panel')
print('  • Zoom to 1:50 000 or closer to see store name labels')
print('  • Layout → Layout Manager to open the print layout')
print('  • Layout → Export as Image / PDF to export your map')
print('─'*52 + '\n')