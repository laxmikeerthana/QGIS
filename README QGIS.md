# 🗺️ RetailMap SF — QGIS Portfolio Project

A professional GIS portfolio project built with **QGIS 3** and **PyQGIS**, mapping 43 retail stores across 14 San Francisco neighborhoods. Demonstrates geospatial data loading, categorized symbology, heatmap visualization, label engineering, and print layout design.

---

## 📁 Files in This Folder

| File | Purpose |
|---|---|
| `stores.geojson` | GeoJSON point layer — 43 SF retail stores |
| `setup_project.py` | PyQGIS script — run once to build the full project |
| `retailmap_sf.qgs` | *(auto-generated)* QGIS project file — open this in QGIS |
| `README_QGIS.md` | This file |

---

## 🚀 Quick Start

### Step 1 — Open QGIS
Open **QGIS Desktop 3.16 or newer**. [(Download QGIS)](https://qgis.org/download/)

### Step 2 — Open the Python Console
Go to **Plugins → Python Console** (or press `Ctrl + Alt + P`)

### Step 3 — Run the setup script
1. Click the **Show Editor** button (📄 icon in the console toolbar)
2. Click **Open Script…** and select `setup_project.py`
3. Click the green **▶ Run** button

The script will automatically:
- Load `stores.geojson` as a styled vector layer
- Add an OpenStreetMap basemap
- Create a rating-weighted heatmap layer
- Configure store name labels
- Build a print-ready A4 layout
- Save the project as **`retailmap_sf.qgs`**

### Step 4 — Explore your project
Open `retailmap_sf.qgs` in QGIS. You're done!

---

## ✨ What's in the Project

### Layers

| Layer | Type | Description |
|---|---|---|
| **SF Retail Stores** | Vector — Points | 43 stores, categorized by retail type |
| **Store Density Heatmap** | Vector — Heatmap | Rating-weighted density visualization (hidden by default) |
| **OpenStreetMap** | Raster — XYZ Tiles | Street basemap |

### Map Features

- **Categorized symbology** — Each of the 6 retail categories has a distinct colour:

  | Category | Colour |
  |---|---|
  | 🛒 Grocery | Teal `#4ECDC4` |
  | 💻 Electronics | Orange `#FF6B35` |
  | 👗 Fashion | Purple `#B57BFF` |
  | 💊 Pharmacy | Green `#2DCC85` |
  | 🏃 Sports | Yellow `#FFC947` |
  | 🏠 Home | Pink `#FF6B9D` |

- **Smart labels** — Store names appear automatically when zoomed to **1:50 000 or closer**, with a white buffer for readability
- **Heatmap layer** — Toggle on the *Store Density Heatmap* layer in the Layers panel to switch to a density view weighted by store rating
- **Print layout** — A ready-to-export A4 landscape layout with title, map frame, legend, and scale bar

---

## 🖨️ Exporting the Map

1. Go to **Project → Layout Manager**
2. Open **"RetailMap SF — Print Layout"**
3. Export via:
   - **Layout → Export as Image…** (PNG, JPEG)
   - **Layout → Export as PDF…**
   - **Layout → Export as SVG…**

---

## 🔧 Customization Tips

| What to change | Where |
|---|---|
| Add more stores | Edit `stores.geojson`, re-run the script |
| Change category colours | Edit the `PALETTE` dict at the top of `setup_project.py` |
| Adjust label zoom threshold | Change `ls.minimumScale = 50000` |
| Change heatmap colours | Edit the `QgsGradientColorRamp` stops |
| Change basemap style | Swap OSM URL for CartoDB, Esri, Stamen, etc. |

**Alternative basemap URLs** (replace the OSM URL in the script):

```
# CartoDB Dark Matter
https://basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png

# CartoDB Positron (light)
https://basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png

# Esri World Imagery
https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
```

---

## 📐 Data Schema

Each feature in `stores.geojson` contains:

| Field | Type | Example |
|---|---|---|
| `id` | Integer | `1` |
| `name` | String | `"Whole Foods Market"` |
| `category` | String | `"Grocery"` |
| `neighborhood` | String | `"SoMa"` |
| `address` | String | `"399 4th St, SoMa"` |
| `rating` | Float | `4.2` |
| `employees` | Integer | `120` |
| `sqft` | Integer | `45000` |

Coordinate system: **WGS 84 / EPSG:4326**

> ⚠️ Data is simulated for portfolio/educational purposes.

---

## 🛠️ Requirements

- QGIS **3.16** or newer *(3.28 LTR recommended)*
- Internet connection for the OSM basemap tile layer

---

*Built with PyQGIS · Part of the RetailMap SF GIS Portfolio*
