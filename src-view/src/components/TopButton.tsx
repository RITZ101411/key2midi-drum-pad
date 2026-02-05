type Props = {
  label?: string
}

export default function TopButton({ label }: Props) {
  return (
    <div className="w-30 h-15 bg-[var(--bg-element)] border-[3.5px] border-[var(--border-accent)] flex items-center justify-center text-[var(--text-default)] text-sm cursor-pointer">
      {label}
    </div>
  )
}
