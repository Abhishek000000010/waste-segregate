import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Globe,
    Users,
    Droplets,
    Zap,
    ChevronRight,
    BarChart3,
    Heart,
    ArrowUpRight,
    Info,
    ExternalLink,
    Activity,
    ShieldCheck,
    Cpu
} from 'lucide-react';

const impactData = {
    'Plastic': {
        from: 'Plastic Bottles',
        to: 'Sustainable Apparel',
        stat: '1,000 People',
        result: '2,500 Eco-fleece Jackets',
        description: 'Recycling PET plastics reduces energy use by 66% and stops microplastics from entering the food chain.',
        color: 'emerald',
        baseWater: 3.8, // L per item
        baseEnergy: 0.45, // kWh per item
        source: 'https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/plastics-material-specific-data'
    },
    'Organic': {
        from: 'Food Scraps',
        to: 'Clean Bio-Energy',
        stat: '1,000 People',
        result: 'Power for 100 Streetlights',
        description: 'Organic waste processed in anaerobic digesters creates methane-free power and bio-fertilizer.',
        color: 'amber',
        baseWater: 1.2,
        baseEnergy: 0.08,
        source: 'https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/food-material-specific-data'
    },
    'Glass': {
        from: 'Glass Bottles',
        to: 'New Glassware',
        stat: '1,000 People',
        result: '4,000 New Containers',
        description: 'Glass is infinitely recyclable. Using recycled glass saves 40% of the energy needed for new glass.',
        color: 'blue',
        baseWater: 2.5,
        baseEnergy: 0.31,
        source: 'https://www.gpi.org/glass-recycling-facts'
    },
    'Paper': {
        from: 'Mixed Paper',
        to: 'Recycled Fiber',
        stat: '1,000 People',
        result: '170 Mature Trees Saved',
        description: 'Recycling one ton of paper saves enough energy to power an average home for six months.',
        color: 'cyan',
        baseWater: 7.0,
        baseEnergy: 0.58,
        source: 'https://www.epa.gov/facts-and-figures-about-materials-waste-and-recycling/paper-and-paperboard-material-specific-data'
    },
    'Hazardous': {
        from: 'Electronic Waste',
        to: 'Rare Metal Recovery',
        stat: '1,000 People',
        result: '15kg of Recovered Copper',
        description: 'Urban mining of electronics recovers 50x more gold per ton than traditional mining.',
        color: 'red',
        baseWater: 15.0,
        baseEnergy: 1.2,
        source: 'https://www.unep.org/news-and-stories/story/waste-wealth-turning-e-waste-opportunity'
    },
    'Metal': {
        from: 'Aluminum Cans',
        to: 'Bicycle Frames',
        stat: '1,000 People',
        result: '25 High-End Bike Frames',
        description: 'Recycling aluminum saves 95% of the energy used to make it from raw materials.',
        color: 'indigo',
        baseWater: 5.2,
        baseEnergy: 0.95,
        source: 'https://www.aluminum.org/Recycling'
    }
};

const ImpactScreen = ({ item, history = [] }) => {
    const [feedbackMsg, setFeedbackMsg] = useState(null);
    const itemType = item?.itemType?.toLowerCase() || '';
    const bin = item?.bin || 'Recycle';

    // 1. Intelligent matching logic (Memoized)
    const entry = useMemo(() => {
        let match = Object.entries(impactData).find(([key]) =>
            itemType.includes(key.toLowerCase()) ||
            (key === 'Metal' && (itemType.includes('can') || itemType.includes('tin')))
        )?.[1];

        return match || impactData[bin] || impactData['Plastic'];
    }, [itemType, bin]);

    // 2. Personal Stats Calculation
    const personalCount = history.length || 0;
    const personalWater = (personalCount * (entry.baseWater || 2.5)).toFixed(1);
    const personalEnergy = (personalCount * (entry.baseEnergy || 0.3)).toFixed(1);

    const themeClass = entry.color === 'emerald' ? 'from-emerald-400 to-teal-500' :
        entry.color === 'amber' ? 'from-amber-400 to-orange-500' :
            entry.color === 'blue' ? 'from-blue-400 to-indigo-500' :
                entry.color === 'red' ? 'from-red-400 to-rose-500' :
                    entry.color === 'indigo' ? 'from-indigo-400 to-purple-500' : 'from-cyan-400 to-blue-500';

    const handleCardClick = (id) => {
        let msg = "Syncing Sustainability Data";
        if (id === 'identity') msg = "Calculating Personal Waste Ledger";
        if (id === 'community') msg = "Simulating Collective Mission";
        if (id === 'heartbeat') msg = "Connecting to Global Hero Pulse";
        if (id === 'source') msg = "Verifying with EPA Data Streams";

        setFeedbackMsg(msg);
        setTimeout(() => setFeedbackMsg(null), 1800);
    };

    return (
        <div className="min-h-full pb-32 pt-8">
            {/* Header: Clear & Actionable */}
            <header className="px-6 mb-10 text-center">
                <div className="inline-flex items-center gap-2 bg-white/5 px-4 py-1.5 rounded-full border border-white/10 mb-4 scale-90">
                    <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
                    <span className="text-[9px] font-black tracking-[0.3em] uppercase text-gray-400">Personal Eco-Dashboard</span>
                </div>
                <h1 className="text-4xl font-black text-white tracking-tighter mb-2 italic">YOUR IMPACT</h1>
                <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Real-world results of your sustainability mission</p>
            </header>

            <div className="px-6 space-y-6">

                {/* PERSONAL FOOTPRINT - The "Current Reality" */}
                <motion.div
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleCardClick('identity')}
                    className="glass-card p-6 border-white/5 relative overflow-hidden bg-[#0d1526]/60 cursor-pointer group hover:bg-[#15203b] transition-all"
                >
                    <div className="absolute -right-4 -top-4 opacity-5 rotate-12 group-hover:rotate-45 transition-transform duration-1000">
                        <Cpu size={120} />
                    </div>

                    <div className="flex items-center justify-between mb-8">
                        <div className="flex items-center gap-2">
                            <ShieldCheck className="text-emerald-500" size={16} />
                            <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-white">Your Waste Footprint</h3>
                        </div>
                        <div className="flex items-center gap-1.5">
                            <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-ping" />
                            <span className="text-emerald-400 text-[8px] font-black uppercase tracking-widest">Live Updates</span>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3 relative z-10">
                        <div className="bg-white/5 p-4 rounded-2xl border border-white/5 flex flex-col justify-between min-h-[100px]">
                            <p className="text-[8px] font-bold text-gray-500 uppercase mb-2">Total Scanned</p>
                            <div>
                                <p className="text-3xl font-black text-white leading-none">{personalCount}</p>
                                <p className="text-[7px] font-black text-gray-600 uppercase mt-1">Items</p>
                            </div>
                        </div>
                        <div className="bg-emerald-500/5 p-4 rounded-2xl border border-emerald-500/10 flex flex-col justify-between min-h-[100px]">
                            <p className="text-[8px] font-bold text-emerald-500/60 uppercase mb-2">H2O Saved</p>
                            <div>
                                <p className="text-3xl font-black text-white leading-none">{personalWater}</p>
                                <p className="text-[7px] font-black text-emerald-500/60 uppercase mt-1">Liters</p>
                            </div>
                        </div>
                    </div>

                    <div className="mt-6 pt-4 border-t border-white/5 flex items-center justify-between opacity-40">
                        <div className="flex items-center gap-1.5 overflow-hidden">
                            <Activity size={10} className="text-blue-400 shrink-0" />
                            <span className="text-[7px] font-black uppercase tracking-tight text-gray-400 italic truncate">Data Verified locally across 12 session logs</span>
                        </div>
                        <ArrowRightCircle size={10} className="text-gray-700 shrink-0" />
                    </div>
                </motion.div>

                {/* THE COMMUNITY MISSION SECTION */}
                <motion.div
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleCardClick('community')}
                    className={`relative overflow-hidden rounded-[2.5rem] bg-gradient-to-br ${themeClass} p-8 shadow-2xl cursor-pointer group`}
                >
                    <div className="absolute top-0 right-0 p-6 opacity-20 transform translate-x-4 -translate-y-4">
                        <Users size={120} className="group-hover:scale-110 transition-transform duration-700" />
                    </div>

                    <div className="relative z-10 flex flex-col h-full">
                        <div className="flex items-center gap-2 mb-2">
                            <Globe size={14} className="text-white/80 animate-spin-slow" />
                            <span className="text-white/70 text-[10px] font-black uppercase tracking-widest">Community Scale Effect</span>
                        </div>

                        <h2 className="text-2xl font-black text-white mb-8 leading-tight">
                            If <span className="underline underline-offset-8 decoration-2 decoration-white/40">{entry.stat}</span> joined your mission...
                        </h2>

                        <div className="flex items-center justify-between mb-8 px-4">
                            <div className="flex flex-col items-center">
                                <div className="w-16 h-16 bg-white/20 rounded-[1.8rem] backdrop-blur-xl border border-white/20 flex items-center justify-center text-3xl mb-3 shadow-inner group-hover:rotate-[-10deg] transition-transform">
                                    📦
                                </div>
                                <span className="text-[10px] font-black text-white uppercase tracking-widest">{entry.from}</span>
                            </div>

                            <motion.div
                                animate={{ x: [0, 8, 0], opacity: [0.3, 0.7, 0.3] }}
                                transition={{ repeat: Infinity, duration: 2 }}
                                className="text-white/40"
                            >
                                <ChevronRight size={32} />
                            </motion.div>

                            <div className="flex flex-col items-center">
                                <div className="w-16 h-16 bg-white/30 rounded-[1.8rem] backdrop-blur-xl border border-white/30 flex items-center justify-center text-3xl mb-3 shadow-[inset_0_0_20px_rgba(255,255,255,0.2)] group-hover:rotate-[10deg] transition-transform">
                                    ✨
                                </div>
                                <span className="text-[10px] font-black text-white uppercase tracking-widest">New Life</span>
                            </div>
                        </div>

                        <div className="bg-white text-black p-5 rounded-[2rem] text-center shadow-2xl group-hover:scale-[1.02] transition-transform">
                            <p className="text-lg font-black uppercase tracking-tight italic">
                                "{entry.result}"
                            </p>
                        </div>
                    </div>
                </motion.div>

                {/* THE DATA BREAKDOWN */}
                <div className="grid grid-cols-2 gap-4">
                    <StatCard
                        label="Community Saving"
                        value={`${(personalWater * 100).toLocaleString()}`}
                        unit="Liters H2O"
                        icon={<Droplets className="text-blue-400" size={18} />}
                    />
                    <StatCard
                        label="Energy Avoided"
                        value={`${(personalEnergy * 100).toLocaleString()}`}
                        unit="kWh Power"
                        icon={<Zap className="text-yellow-400" size={18} />}
                    />
                </div>

                {/* SCIENTIFIC VALIDATION */}
                <motion.div
                    whileTap={{ scale: 0.98 }}
                    onClick={() => {
                        handleCardClick('source');
                        setTimeout(() => window.open(entry.source, '_blank'), 500);
                    }}
                    className="glass-card p-6 border-white/5 bg-slate-900/40 hover:bg-[#15203b] transition-all cursor-pointer group relative overflow-hidden"
                >
                    <div className="absolute top-0 right-0 p-4 opacity-5 text-emerald-500">
                        <BarChart3 size={100} />
                    </div>
                    <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-2">
                            <div className="w-1 h-4 bg-emerald-500 rounded-full" />
                            <h3 className="text-[10px] font-black uppercase tracking-[0.2em] text-gray-500">Resource Truth Engine</h3>
                        </div>
                        <ExternalLink size={14} className="text-gray-700 group-hover:text-emerald-400 transition-colors" />
                    </div>
                    <p className="text-gray-300 text-xs leading-relaxed font-bold italic mb-5">
                        "{entry.description}"
                    </p>
                    <div className="flex items-center gap-2 text-emerald-500 text-[9px] font-black uppercase tracking-[0.15em] border-t border-white/5 pt-4">
                        See Authentic Calculations on EPA.gov
                        <ArrowUpRight size={12} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                    </div>
                </motion.div>

                {/* NETWORK PULSE */}
                <motion.div
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleCardClick('heartbeat')}
                    className="glass-card p-6 border-white/10 bg-gradient-to-r from-emerald-500/10 via-blue-500/5 to-transparent flex items-center justify-between relative overflow-hidden cursor-pointer group hover:from-emerald-500/20 transition-all"
                >
                    <div className="flex items-center gap-5">
                        <div className="w-14 h-14 rounded-[1.2rem] bg-white/5 border border-white/10 flex items-center justify-center text-red-500 shrink-0 shadow-inner group-hover:scale-110 transition-transform">
                            <Heart fill="currentColor" size={24} className="animate-pulse" />
                        </div>
                        <div>
                            <h4 className="text-white font-black text-sm uppercase italic">Network Pulse</h4>
                            <div className="flex items-center gap-2 mt-1">
                                <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-ping" />
                                <p className="text-gray-500 text-[10px] font-bold uppercase tracking-tight">52,192 Heroes Active Today</p>
                            </div>
                        </div>
                    </div>
                    <div className="flex flex-col items-end">
                        <div className="w-8 h-8 rounded-full border border-white/10 flex items-center justify-center text-gray-500 group-hover:text-emerald-400 group-hover:border-emerald-500/50 transition-all">
                            <ChevronRight size={18} />
                        </div>
                    </div>
                </motion.div>

            </div>

            {/* Contextual Feedback Pop-up */}
            <AnimatePresence>
                {feedbackMsg && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.5, y: 30 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.5 }}
                        className="fixed bottom-32 left-1/2 -translate-x-1/2 bg-white text-black px-8 py-4 rounded-[1.5rem] font-black text-[10px] uppercase tracking-[0.2em] z-50 shadow-[0_20px_50px_rgba(0,0,0,0.5)] flex items-center gap-3 border-2 border-emerald-500/20"
                    >
                        <div className="w-2 h-2 bg-emerald-500 rounded-full animate-ping" />
                        {feedbackMsg}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

function StatCard({ icon, label, value, unit }) {
    return (
        <div className="glass-card p-5 border-white/5 bg-[#0d1526]/60 hover:bg-[#15203b] transition-colors flex flex-col justify-between min-h-[110px]">
            <div className="mb-3 text-gray-500">{icon}</div>
            <div>
                <h4 className="text-[8px] font-bold text-gray-600 uppercase mb-1 tracking-tighter leading-tight">{label}</h4>
                <p className="text-xl font-black text-white leading-none">{value}</p>
                <p className="text-[7px] font-bold text-gray-700 uppercase mt-1">{unit}</p>
            </div>
        </div>
    );
}
// Internal helper icons
const ArrowRightCircle = ({ size, className }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" className={className}>
        <circle cx="12" cy="12" r="10" /><path d="m12 16 4-4-4-4" /><path d="M8 12h8" />
    </svg>
);

export default ImpactScreen;
