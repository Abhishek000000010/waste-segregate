import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Camera, ClipboardList, BarChart3, Globe2, Leaf, Smartphone, X } from 'lucide-react'
import ScanScreen from './components/ScanScreen'
import ItemDetailScreen from './components/ItemDetailScreen'
import InsightsScreen from './components/InsightsScreen'
import ImpactScreen from './components/ImpactScreen'
import ImpactDashboard from './components/ImpactDashboard'
import { WASTE_KNOWLEDGE } from './data/wasteData'

function App() {
  const [activeTab, setActiveTab] = useState('scan')
  const [selectedItem, setSelectedItem] = useState(null)
  const [scanHistory, setScanHistory] = useState([])
  const [showMobileNotice, setShowMobileNotice] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowMobileNotice(false)
    }, 4500)
    return () => clearTimeout(timer)
  }, [])

  // Handle navigation to details
  const handleShowDetails = (item, image = null) => {
    // If an image is provided, attach it to the item object
    const itemWithImage = image ? { ...item, capturedImage: image } : item;
    setSelectedItem(itemWithImage)
    // Add to history if not already there (simple unique check by type or ID)
    setScanHistory(prev => [itemWithImage, ...prev].slice(0, 20))
    setActiveTab('details')
  }

  // Render active screen
  const renderScreen = () => {
    switch (activeTab) {
      case 'scan':
        return <ScanScreen onShowDetails={handleShowDetails} />
      case 'details':
        return <ItemDetailScreen item={selectedItem} />
      case 'insights':
        return <InsightsScreen history={scanHistory} onItemClick={handleShowDetails} />
      case 'impact':
        return <ImpactScreen item={selectedItem} history={scanHistory} />
      default:
        return <ScanScreen onShowDetails={handleShowDetails} />
    }
  }

  return (
    <div className="min-h-screen bg-[#0a0f1e] text-white selection:bg-emerald-500/30 overflow-hidden relative">
      {/* Background Mesh */}
      <div className="fixed inset-0 bg-mesh opacity-50 pointer-events-none" />

      {/* Mobile Experience Notice */}
      <AnimatePresence>
        {showMobileNotice && (
          <motion.div
            initial={{ y: -100, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -100, opacity: 0 }}
            className="fixed top-8 left-1/2 -translate-x-1/2 z-[100] w-[92%] max-w-sm"
          >
            <div className="glass-card relative overflow-hidden p-5 bg-slate-900 shadow-[0_20px_60px_rgba(0,0,0,0.6)] border-white/10 group">
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-500/10 via-transparent to-blue-500/10 opacity-50" />
              <div className="relative z-10 flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
                  <Smartphone className="animate-pulse" size={24} />
                </div>
                <div className="flex-1">
                  <h4 className="text-[10px] font-black uppercase tracking-[0.2em] text-emerald-500 mb-1">Tech Recommendation</h4>
                  <p className="text-white font-bold text-xs leading-tight">Use mobile for the best recycling experience.</p>
                </div>
                <button
                  onClick={() => setShowMobileNotice(false)}
                  className="p-2 hover:bg-white/5 rounded-full text-gray-500 hover:text-white transition-colors"
                >
                  <X size={16} />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Impact Dashboard */}
      <ImpactDashboard history={scanHistory} wasteKnowledge={WASTE_KNOWLEDGE} />

      {/* Top Banner (Optional for Hackathon feel) */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-emerald-500 via-blue-500 to-emerald-500 z-50 animate-pulse" />

      {/* Main Content Area */}
      <main className="relative h-screen pb-24 pt-20 overflow-y-auto">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, scale: 0.98, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 1.02, y: -10 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className="h-full"
          >
            {renderScreen()}
          </motion.div>
        </AnimatePresence>
      </main>

      {/* Premium Glass Bottom Navigation */}
      <nav className="fixed bottom-4 left-3 right-3 sm:bottom-6 sm:left-6 sm:right-6 z-50">
        <div className="glass-card flex justify-between sm:justify-around items-center p-2 sm:p-3 shadow-[0_8px_32px_rgba(0,0,0,0.5)] bg-slate-900/80 backdrop-blur-xl">
          <NavButton
            active={activeTab === 'scan'}
            onClick={() => setActiveTab('scan')}
            icon={<Camera size={20} />}
            label="Scan"
            color="emerald"
          />
          <NavButton
            active={activeTab === 'details'}
            onClick={() => setActiveTab('details')}
            icon={<ClipboardList size={20} />}
            label="Details"
            color="emerald"
          />
          <NavButton
            active={activeTab === 'insights'}
            onClick={() => setActiveTab('insights')}
            icon={<BarChart3 size={20} />}
            label="Insights"
            color="blue"
          />
          <NavButton
            active={activeTab === 'impact'}
            onClick={() => setActiveTab('impact')}
            icon={<Globe2 size={20} />}
            label="Impact"
            color="blue"
          />
        </div>
      </nav>
    </div>
  )
}

function NavButton({ active, onClick, icon, label, color }) {
  const activeClass = color === 'emerald'
    ? 'bg-emerald-500 text-white shadow-[0_0_20px_rgba(16,185,129,0.3)]'
    : 'bg-blue-600 text-white shadow-[0_0_20px_rgba(37,99,235,0.3)]'

  return (
    <button
      onClick={onClick}
      className={`flex flex-col items-center gap-1 p-2 px-3 sm:px-5 rounded-xl sm:rounded-2xl transition-all duration-300 ${active ? activeClass : 'text-gray-500 hover:text-white'
        }`}
    >
      <div className={`${active ? 'scale-110' : 'scale-100'} transition-transform`}>
        {icon}
      </div>
      <span className={`text-[9px] sm:text-[10px] font-black uppercase tracking-widest ${active ? 'block' : 'hidden sm:block'}`}>
        {label}
      </span>
    </button>
  )
}

export default App
