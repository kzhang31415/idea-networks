import React, { useState, useEffect } from 'react';
import data from './data/data.json'; //Remove this once the backend is set up
import { ForceGraph } from "./components/forceGraph";
import './App.css';

function App() {
  // const [data, setData] = useState([{}]);
  const [input, setInput] = useState('');

  const handleTextareaChange = (e) => {
    setInput(e.target.value);
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(input);
    //fetch('/api/make-graph?input=' + input).then(
    //  res => res.json()
    //).then(
    //  data => {
    //  setData(data);
    //  console.log(data);
    //})
  }

  const nodeHoverTooltip = React.useCallback((node) => {
    return `<div>${node.name}</div>`;
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Idea Networks</h1>
        <form onSubmit={handleSubmit}>
          <textarea
            value={input}
            onChange={handleTextareaChange}
          />
          <br></br>
          <button type="submit">Make graph!</button>
        </form>
      </header>
      <section className="Main">
        <ForceGraph linksData={(typeof data === 'undefined') ? {} : data.links} nodesData={(typeof data === 'undefined') ? {} : data.nodes} nodeHoverTooltip={nodeHoverTooltip} />
      </section>
    </div>
  );
}

export default App;