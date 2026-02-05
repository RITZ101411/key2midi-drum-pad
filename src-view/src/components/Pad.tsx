type Props = {
  index: number
}

export default function Pad({ index }: Props) {
  return (
    <div className="flex flex-col">
      <div className="w-30 h-30 aspect-square bg-[var(--bg-element)] border-2 border-[var(--border-default)] transition-colors pad" id={`pad${index}`} />
      <div className="text-[var(--text-default)] text-xs mt-1">PAD{index + 1}</div>
    </div>
  )
}
