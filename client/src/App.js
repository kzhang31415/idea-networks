import React, { useState, useEffect } from 'react';
// import data from './data/data.json'; //Remove this once the backend is set up
import { ForceGraph } from "./components/forceGraph";
import './App.css';

function App() {
  const [data, setData] = useState({nodes: [{"id": 1, "name": "Example 1", "type": "interior"}, {"id": 2, "name": "Example 2", "type": "interior"}], links: [{"source": 1, "target": 2}]});
  const [input1, setInput1] = useState('');
  const [input2, setInput2] = useState('');
  
  const handleTextareaChange1 = (e) => {
    setInput1(e.target.value);
  }
  const handleTextareaChange2 = (e) => {
    setInput2(e.target.value);
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    //console.log('/apis/make_graph?s1=' + input1.split(" ").join("_") + '&s2=' + input2.split(" ").join("_"));

    fetch('/make_graph?s1=' + input1.split(" ").join("_") + '&s2=' + input2.split(" ").join("_")).then(
     res => res.json()
    ).then(
     data => {
     setData(data);
    });
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
            value={input1}
            onChange={handleTextareaChange1}
          />
          <textarea
            value={input2}
            onChange={handleTextareaChange2}
          />
          <br></br>
          <button type="submit">Make graph!</button>
        </form>
      </header>
      <section className="Main">
        <ForceGraph linksData={data.links} nodesData={data.nodes} nodeHoverTooltip={nodeHoverTooltip} />
      </section>
    </div>
  );
}

export default App;