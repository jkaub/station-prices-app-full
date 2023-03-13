import "./StationsFilter.css";
import { useState } from "react";

export default function StationsFilter(props) {
  const fuelTypes = ["E10", "E85", "Gazole", "GPLc", "SP95", "SP98"];

  const [gasType, setGasType] = useState("SP95");
  const [postalCode, setPostalCode] = useState("");

  const handleChangeDropdown = (event) => {
    setGasType(event.target.value);
  };

  const handleChangeTextArea = (event) => {
    const newValue = event.target.value;
    if (/^\d{0,5}$/.test(newValue)) {
      setPostalCode(newValue);
    }
  };

  const handleButtonClick = () => {
    props.ApiCallAndUpdateState(gasType, postalCode);
  };

  return (
    <div className="search-form">
      <input
        className={"general-input" + (props.apiError ? " input-error" : "")}
        type="text"
        placeholder="Postal Code"
        onChange={handleChangeTextArea}
        value={postalCode}
      />
      <select
        value={gasType}
        className="general-input"
        onChange={handleChangeDropdown}
      >
        {fuelTypes.map((e) => (
          <option value={e} key={e}>
            {e}
          </option>
        ))}
      </select>
      <button className="send-request-button" onClick={handleButtonClick}>
        Find Stations
      </button>
    </div>
  );
}
