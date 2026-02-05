export const DrumPad = () => {
  return (
    <div className="relative w-24 h-24 cursor-pointer select-none">
      {/* グラデーション枠 */}
      <div className="absolute inset-0 rounded-md bg-gradient-to-r from-red-500 to-red-400 p-[3px]">
        {/* 内側の黒背景 */}
        <div className="w-full h-full bg-default-strong rounded-md flex items-center justify-center text-white text-xl font-bold">
          {/* 中央のラベルやアイコンはここに */}
        </div>
      </div>
    </div>
  );
};
