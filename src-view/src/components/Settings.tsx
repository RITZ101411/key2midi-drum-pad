import { useState, useEffect } from 'react'

type Config = {
  velocity: number
  pads: Array<{ key: string; note: number }>
}

type Props = {
  onClose: () => void
}

export const Settings = ({ onClose }: Props) => {
  const [config, setConfig] = useState<Config | null>(null)
  const [velocity, setVelocity] = useState(80)
  const [pads, setPads] = useState<Array<{ key: string; note: number }>>([])

  useEffect(() => {
    const loadConfig = async () => {
      try {
        const cfg = await (window as any).pywebview.api.get_config()
        setConfig(cfg)
        setVelocity(cfg.velocity)
        setPads(cfg.pads)
      } catch (e) {
        console.error('Failed to load config:', e)
      }
    }
    loadConfig()
  }, [])

  const handleSave = async () => {
    if (!config) return
    
    const newConfig = {
      velocity,
      pads
    }
    
    try {
      await (window as any).pywebview.api.save_config(newConfig)
      onClose()
    } catch (e) {
      console.error('Failed to save config:', e)
    }
  }

  const updatePad = (index: number, field: 'key' | 'note', value: string | number) => {
    const newPads = [...pads]
    newPads[index] = { ...newPads[index], [field]: value }
    setPads(newPads)
  }

  if (!config) {
    return <div className="text-white">Loading...</div>
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-default/80 p-6 rounded-lg w-[600px] max-h-[80vh] overflow-y-auto shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <h2 className="text-white text-xl mb-4">Settings</h2>
        
        <div className="mb-4">
          <label className="text-gray-light text-sm block mb-2">
            Velocity (1-127): {velocity}
          </label>
          <input
            type="range"
            min="1"
            max="127"
            value={velocity}
            onChange={(e) => setVelocity(Number(e.target.value))}
            className="w-full"
          />
        </div>

        <div className="mb-4">
          <h3 className="text-white text-lg mb-2">Pad Mappings</h3>
          <div className="grid grid-cols-2 gap-2">
            {pads.map((pad, i) => (
              <div key={i} className="flex gap-2 items-center bg-default-strong p-2 rounded">
                <span className="text-gray-light text-sm w-12">PAD{i+1}</span>
                <input
                  type="text"
                  value={pad.key}
                  onChange={(e) => updatePad(i, 'key', e.target.value)}
                  className="bg-gray-dark text-white px-2 py-1 rounded w-12 text-center text-sm"
                  maxLength={1}
                />
                <span className="text-gray-light text-sm">→</span>
                <input
                  type="number"
                  value={pad.note}
                  onChange={(e) => updatePad(i, 'note', Number(e.target.value))}
                  className="bg-gray-dark text-white px-2 py-1 rounded w-16 text-sm"
                  min="0"
                  max="127"
                />
              </div>
            ))}
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={handleSave}
            className="flex-1 bg-blue hover:bg-blue-hover text-white px-4 py-2 rounded"
          >
            Save
          </button>
          <button
            onClick={onClose}
            className="flex-1 bg-gray-dark hover:bg-gray-medium text-white px-4 py-2 rounded"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  )
}
