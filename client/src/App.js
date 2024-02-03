import React, { useState, useEffect } from 'react';
import data from './data/data.json';
import { ForceGraph } from "./components/forceGraph";
import './App.css';

function App() {
  // const [data, setData] = useState([{}]);
  // useEffect(() => {
  //     fetch('/members').then(
  //       res => res.json()
  //     ).then(
  //       data => {
  //         setData(data);
  //         console.log(data);
  //       }
  //     )
  // }, []); //Once this is uncommented, the data.json file will not be used and the data will be fetched from the server


  const nodeHoverTooltip = React.useCallback((node) => {
    return `<div>${node.name}</div>`;
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        Force Graph Example 
      </header>
      <section className="Main">
        <ForceGraph linksData={(typeof data.links === 'undefined') ? {} : data.links} nodesData={(typeof data.links === 'undefined') ? {} : data.nodes} nodeHoverTooltip={nodeHoverTooltip} />
      </section>
    </div>
  );
}

export default App;