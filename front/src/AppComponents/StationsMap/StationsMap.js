import "./StationsMap.css";
import Plot from "react-plotly.js";
import { v4 as uuidv4 } from "uuid";
import { calcPointsOnCircle } from "./utils/drawCircle";

export default function StationsMap(props) {
  const { REACT_APP_API_KEY } = process.env;
  const COLOR_PRICE_THRESHOLD = 0.1;
  const mapDistZoom = {
    1: 14.0,
    2: 13.45,
    3: 12.9,
    4: 12.35,
    5: 11.8,
    6: 11.6,
    7: 11.4,
    8: 11.2,
    9: 11.0,
    10: 10.8,
    11: 10.68,
    12: 10.56,
    13: 10.44,
    14: 10.32,
    15: 10.2,
    16: 10.12,
    17: 10.04,
    18: 9.96,
    19: 9.88,
    20: 9.8,
    21: 9.73,
    22: 9.66,
    23: 9.59,
    24: 9.52,
    25: 9.45,
    26: 9.4,
    27: 9.35,
    28: 9.3,
    29: 9.25,
    30: 9.2,
  };

  const zoom = mapDistZoom[props.distanceFilter];
  const pointsOnCircle = calcPointsOnCircle(
    props.latCity,
    props.lonCity,
    props.distanceFilter,
    100
  );

  const circleTrace = {
    fill: "toself",
    fillcolor: "rgba(1,1,1,0.2)",
    lat: pointsOnCircle.map((e) => e[0]),
    lon: pointsOnCircle.map((e) => e[1]),
    marker: { color: "black", size: 45 },
    mode: "lines",
    opacity: 0.8,
    showlegend: false,
    type: "scattermapbox",
    uid: uuidv4(),
    hoverinfo: "skip",
  };

  const stationsBorder = {
    lat: props.stationsData.map((e) => e["latitude"]),
    lon: props.stationsData.map((e) => e["longitude"]),
    marker: { color: "black", size: 45 },
    mode: "markers",
    opacity: 0.8,
    showlegend: false,
    text: props.stationsData.map((e) => e["price_per_L"].toString() + "€/L"),
    type: "scattermapbox",
    uid: uuidv4(),
  };

  const stationsPriceColor = {
    lat: props.stationsData.map((e) => e["latitude"]),
    lon: props.stationsData.map((e) => e["longitude"]),
    zmin: props.avgPrice,
    zmax: props.avgPrice,
    marker: {
      color: props.stationsData.map((e) => {
        var price = e["price_per_L"];
        if (price > props.avgPrice * (1 + COLOR_PRICE_THRESHOLD)) {
          price = props.avgPrice * (1 + COLOR_PRICE_THRESHOLD);
        }
        if (price < props.avgPrice * (1 - COLOR_PRICE_THRESHOLD)) {
          price = props.avgPrice * (1 - COLOR_PRICE_THRESHOLD);
        }
        return price;
      }),
      colorscale: [
        [0.0, "rgb(39,100,25)"],
        [0.1, "rgb(77,146,33)"],
        [0.2, "rgb(127,188,65)"],
        [0.3, "rgb(184,225,134)"],
        [0.4, "rgb(230,245,208)"],
        [0.5, "rgb(247,247,247)"],
        [0.6, "rgb(253,224,239)"],
        [0.7, "rgb(241,182,218)"],
        [0.8, "rgb(222,119,174)"],
        [0.9, "rgb(197,27,125)"],
        [1.0, "rgb(142,1,82)"],
      ],
      size: 40,
    },
    mode: "markers",
    opacity: 0.7,
    showlegend: false,
    text: props.stationsData.map((e) => e["price_per_L"].toString() + "€/L"),
    type: "scattermapbox",
    uid: uuidv4(),
    hovertemplate: "%{text}<extra></extra>",
  };

  const stationIconsTrace = {
    lat: props.stationsData.map((e) => e["latitude"]),
    lon: props.stationsData.map((e) => e["longitude"]),
    marker: { color: "white", size: 14, symbol: "fuel" },
    mode: "markers",
    showlegend: false,
    text: props.stationsData.map((e) => e["price_per_L"].toString() + "€/L"),
    type: "scattermapbox",
    uid: uuidv4(),
    opacity: 1,
    hovertemplate: "%{text}<extra></extra>",
  };

  const pointLocation = {
    lat: [props.latCity],
    lon: [props.lonCity],
    marker: { color: "red", size: 5 },
    mode: "markers",
    opacity: 1,
    showlegend: false,
    type: "scattermapbox",
    uid: uuidv4(),
    hoverinfo: "skip",
  };

  const data = [
    circleTrace,
    stationsBorder,
    stationsPriceColor,
    stationIconsTrace,
    pointLocation,
  ];
  const layout = {
    mapbox: {
      accesstoken: REACT_APP_API_KEY,
      center: { lat: props.latCity, lon: props.lonCity },
      style: "streets",
      zoom: zoom,
    },
    margin: { b: 0, l: 0, r: 0, t: 0 },
    autosize: true,
  };

  return (
    <div className="component-embbeder">
      <Plot
        data={data}
        layout={layout}
        style={{ height: "100%", width: "100%" }}
        useResizeHandler={true}
      />
    </div>
  );
}
