import React, { useEffect, useState } from 'react';

const ROWS = 20;
const COLS = 10;

function App() {
  const [state, setState] = useState(null);

  const fetchState = async (action=null) => {
    const res = await fetch('http://127.0.0.1:5000/move', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({action})
    });
    const data = await res.json();
    setState(data);
  };

  const restartGame = async () => {
    const res = await fetch('http://127.0.0.1:5000/restart', {
      method: 'POST'
    });
    const data = await res.json();
    setState(data);
  };

  useEffect(() => {
    const interval = setInterval(()=>fetchState(), 400);
    return ()=>clearInterval(interval);
  }, []);

  useEffect(() => {
    const handle = (e) => {
      if (e.key==='ArrowLeft') fetchState('left');
      if (e.key==='ArrowRight') fetchState('right');
      if (e.key==='ArrowDown') fetchState('down');
      if (e.key==='ArrowUp') fetchState('rotate');
    };
    window.addEventListener('keydown', handle);
    return ()=>window.removeEventListener('keydown', handle);
  }, []);

  if (!state) return <div>Loading...</div>;

  const grid = state.grid.map(row=>row.slice());

  const { piece, x, y } = state;
  if (piece) {
    piece.shape.forEach((r,i)=>{
      r.forEach((val,j)=>{
        if(val){
          const px = x+j;
          const py = y+i;
          if(py>=0) grid[py][px] = piece.color;
        }
      });
    });
  }

  return (
    <div style={{
      display:'flex',
      flexDirection:'column',
      alignItems:'center',
      justifyContent:'center',
      height:'100vh',
      background:'#111',
      color:'white'
    }}>
      <h1 style={{fontSize:'36px'}}>🎮 TETRIS</h1>
      <h3>Score: {state.score}</h3>
      {state.game_over && <h1 style={{color:'red'}}>GAME OVER</h1>}

      <button onClick={restartGame} style={{
        margin:'10px',
        padding:'10px 20px',
        fontSize:'16px',
        background:'#28a745',
        color:'white',
        border:'none',
        borderRadius:'5px',
        cursor:'pointer'
      }}>
        🔄 Restart
      </button>

      <div style={{
        display:'grid',
        gridTemplateColumns:`repeat(${COLS}, 35px)`,
        gap:'2px',
        background:'#222',
        padding:'10px'
      }}>
        {grid.flat().map((cell, i)=>(
          <div key={i} style={{
            width:35,
            height:35,
            background: cell || '#000',
            borderRadius:'4px'
          }}/>
        ))}
      </div>
    </div>
  );
}

export default App;