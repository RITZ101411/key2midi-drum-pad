import { DrumPad } from "./components/Pad";
import "./styles/index.css";
import { useState, useEffect } from "react";

function App() {
  const [activePads, setActivePads] = useState<Map<number, number>>(new Map());

  useEffect(() => {
    const handlePadPress = (e: CustomEvent) => {
      const { index, velocity } = e.detail;
      setActivePads(prev => new Map(prev).set(index, velocity));
    };

    const handlePadRelease = (e: CustomEvent) => {
      const { index } = e.detail;
      setActivePads(prev => {
        const next = new Map(prev);
        next.delete(index);
        return next;
      });
    };

    window.addEventListener('padPress', handlePadPress as EventListener);
    window.addEventListener('padRelease', handlePadRelease as EventListener);
    return () => {
      window.removeEventListener('padPress', handlePadPress as EventListener);
      window.removeEventListener('padRelease', handlePadRelease as EventListener);
    };
  }, []);

  return (
    <div className="p-4 flex justify-center">
      <div className="grid grid-cols-4 gap-x-4 gap-y-1">
        {Array.from({ length: 16 }, (_, i) => (
          <DrumPad 
            key={i} 
            index={i} 
            isActive={activePads.has(i)} 
            velocity={activePads.get(i) || 0}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
