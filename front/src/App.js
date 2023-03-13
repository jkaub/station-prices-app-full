import "./App.css";
import StationsFilter from "./AppComponents/StationsFilter/StationsFilter";
import StationsMap from "./AppComponents/StationsMap/StationsMap";
import StationsTable from "./AppComponents/StationsTable/StationsTable";
import ReactSlider from "react-slider";
import { useState, useEffect } from "react";

export default function App() {
  //Define our state variables with the useState hook
  const [citySearch, setCitySearch] = useState("");
  const [gasTypeSearch, setGasTypeSearch] = useState("");
  const [stationsData, setStationsData] = useState([]);
  const [latCity, setLatCity] = useState(0);
  const [lonCity, setLonCity] = useState(0);
  const [distanceFilter, setDistanceFilter] = useState(5);
  const [apiError, setApiError] = useState(false);
  const APIURL = "http://0.0.0.0:8000";

  const filteredData = stationsData.filter(
    (row) => row.distance <= distanceFilter
  );

  const sumPrice = stationsData.reduce(
    (total, value) => total + value["price_per_L"],
    0
  );

  const avgPrice = sumPrice / stationsData.length;
  const ApiCallAndUpdateState = (gasType, postalCode) => {
    fetch(`${APIURL}/stations?oil_type=${gasType}&postal_code=${postalCode}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Problem with the API...");
        }
        return res.json();
      })
      .then((data) => {
        setStationsData([...data["station_infos"]]);
        setLonCity(data["lon"]);
        setLatCity(data["lat"]);
        setGasTypeSearch(gasType);
        setCitySearch(data["city"]);
        setApiError(false);
      })
      .catch((error) => {
        setApiError(true);
      });
  };

  useEffect(() => {
    ApiCallAndUpdateState("SP98", "75001");
  }, []);

  return (
    <div className="App">
      <header className="header">
        <h1 className="h1-searchbar">Gas Station Finder</h1>
      </header>
      <div className="main-components">
        <div className="left-section">
          <StationsFilter
            ApiCallAndUpdateState={ApiCallAndUpdateState}
            apiError={apiError}
          />
          <ReactSlider
            className="horizontal-slider"
            markClassName="example-mark"
            min={1}
            max={30}
            value={distanceFilter}
            onAfterChange={(e) => setDistanceFilter(e)}
            thumbClassName="example-thumb"
            trackClassName="example-track"
            renderThumb={(props, state) => (
              <div {...props}>{state.valueNow}</div>
            )}
          />
          <h2 style={{ padding: "1px", margin: "2px", textAlign: "center" }}>
            {citySearch} - {gasTypeSearch}
          </h2>
          <StationsTable
            stationsData={filteredData}
            gasTypeSearch={gasTypeSearch}
            citySearch={citySearch}
          />
        </div>
        <StationsMap
          stationsData={filteredData}
          lonCity={lonCity}
          latCity={latCity}
          distanceFilter={distanceFilter}
          avgPrice={avgPrice}
        />
      </div>
    </div>
  );
}
