import { useState } from 'react'

type Props = {
  onClose: () => void
}

type UpdateInfo = {
  version: string
  url: string
  download_url: string | null
  notes: string
}

export const UpdateDialog = ({ onClose }: Props) => {
  const [checking, setChecking] = useState(false)
  const [updateInfo, setUpdateInfo] = useState<UpdateInfo | null>(null)
  const [downloading, setDownloading] = useState(false)

  const checkForUpdates = async () => {
    setChecking(true)
    try {
      const info = await (window as any).pywebview.api.check_updates()
      setUpdateInfo(info)
    } catch (e) {
      console.error('Failed to check updates:', e)
    }
    setChecking(false)
  }

  const downloadUpdate = async () => {
    if (!updateInfo?.download_url) return
    
    setDownloading(true)
    try {
      await (window as any).pywebview.api.download_and_install_update(updateInfo.download_url)
    } catch (e) {
      console.error('Failed to download update:', e)
    }
    setDownloading(false)
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-default/90 p-6 rounded-lg w-96 shadow-2xl" onClick={(e) => e.stopPropagation()}>
        <h2 className="text-white text-xl mb-4">Check for Updates</h2>
        
        {!updateInfo && !checking && (
          <div className="mb-4">
            <p className="text-gray-light text-sm mb-4">Click to check for the latest version</p>
            <button
              onClick={checkForUpdates}
              className="w-full bg-blue hover:bg-blue-hover text-white px-4 py-2 rounded"
            >
              Check for Updates
            </button>
          </div>
        )}

        {checking && (
          <div className="mb-4 text-center">
            <p className="text-gray-light text-sm">Checking for updates...</p>
          </div>
        )}

        {updateInfo && (
          <div className="mb-4">
            <p className="text-white text-lg mb-2">New version available: {updateInfo.version}</p>
            {updateInfo.notes && (
              <div className="bg-default-strong p-3 rounded mb-3 max-h-40 overflow-y-auto">
                <p className="text-gray-light text-sm whitespace-pre-wrap">{updateInfo.notes}</p>
              </div>
            )}
            {updateInfo.download_url ? (
              <button
                onClick={downloadUpdate}
                disabled={downloading}
                className="w-full bg-blue hover:bg-blue-hover text-white px-4 py-2 rounded disabled:opacity-50"
              >
                {downloading ? 'Downloading...' : 'Download & Install'}
              </button>
            ) : (
              <a
                href={updateInfo.url}
                target="_blank"
                rel="noopener noreferrer"
                className="block w-full bg-blue hover:bg-blue-hover text-white px-4 py-2 rounded text-center"
              >
                View on GitHub
              </a>
            )}
          </div>
        )}

        {!updateInfo && !checking && updateInfo === null && (
          <div className="mb-4">
            <p className="text-gray-light text-sm">You're running the latest version!</p>
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full bg-gray-dark hover:bg-gray-medium text-white px-4 py-2 rounded"
        >
          Close
        </button>
      </div>
    </div>
  )
}
