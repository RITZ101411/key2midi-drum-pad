type Props = {
  index: number
  isActive: boolean
  velocity: number
}

export const DrumPad = ({ index, isActive, velocity }: Props) => {
  const handleMouseDown = () => {
    (window as any).pywebview.api.pad_press(index);
  };

  const handleMouseUp = () => {
    (window as any).pywebview.api.pad_release(index);
  };

  return (
    <div className="flex flex-col">
      <div 
        className="relative w-24 h-24 cursor-pointer select-none"
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <div className={`absolute inset-0 rounded-md p-[3px] ${
          isActive ? 'bg-gradient-to-r from-red-500 to-red-400' : 'bg-gradient-to-r from-gray-700 to-gray-700'
        }`}>
          <div className="w-full h-full bg-default-strong rounded-md flex items-center justify-center text-white text-xl font-bold"></div>
        </div>
      </div>
      <div className="flex gap-2 text-xs mt-1">
        <span className="text-gray-400">PAD{index + 1}</span>
        {velocity > 0 && <span className="text-red-400">V:{velocity}</span>}
      </div>
    </div>
  )
}
