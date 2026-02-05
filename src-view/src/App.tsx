import { DrumPad } from "./components/Pad";
import "./styles/index.css";

function App() {
  const pads = Array.from({ length: 16 }, (_, i) => `Pad ${i + 1}`);

  return (
    <div className="p-4 flex justify-center">
      <div className="grid grid-cols-4 gap-4">
        {pads.map((_, index) => (
          <DrumPad key={index} />
        ))}
      </div>
    </div>
  );
}

export default App;
