import TopButton from './components/TopButton'
import Pad from './components/Pad'

function App() {
  return (
    <div className="p-5 bg-[var(--bg-main)] font-sans">
      <div className="flex gap-6 mb-2">
        <TopButton label="PAD設定" />
        <TopButton />
        <TopButton />
        <TopButton />
      </div>
      <div className="grid grid-cols-4 gap-6">
        {Array.from({ length: 16 }, (_, i) => (
          <Pad key={i} index={i} />
        ))}
      </div>
    </div>
  )
}

export default App
