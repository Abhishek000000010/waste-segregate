export const WASTE_KNOWLEDGE = {
    'bottle': {
        image: '/assets/items/bottle.png',
        transformedImage: '/assets/transformed/apparel.png',
        fun_fact: "Plastic bottles can take up to 450 years to decompose in a landfill. Only about 9% of all plastic ever made has been recycled.",
        transformation: "Shredded into high-performance polyester fibers for sustainable soccer jerseys and fleece jackets.",
        impact: "Recycling one ton of PET bottles saves 3.8 barrels of oil and prevents 1.5 tons of carbon emissions.",
        tips: [
            "Empty all liquids and rinse briefly to prevent contamination.",
            "Crush the bottle to save space in the recycling bin.",
            "Keep the cap on; most modern facilities can process them together."
        ],
        numericalImpact: { co2: 150, water: 2500, energy: 30 }
    },
    'cup': {
        image: '/assets/items/cup.png',
        transformedImage: '/assets/transformed/tiles.png',
        fun_fact: "Ceramic cups are made from natural clay but can take thousands of years to decompose in a landfill. Reusing a single cup can save hundreds of paper alternatives.",
        transformation: "Crushed and pulverized into high-durability aggregate for stylish eco-friendly floor tiles and kitchen backsplashes.",
        impact: "Recycling ceramic prevents the mining of new clay and reduces kiln energy consumption by 15%.",
        tips: [
            "If just chipped, consider repairing with 'Kintsugi' or repurposing as a planter.",
            "Check if your local facility accepts ceramic 'hardcore' for construction fill.",
            "Ceramic is NOT accepted in regular glass recycling bins."
        ],
        numericalImpact: { co2: 80, water: 500, energy: 15 }
    },
    'book': {
        image: '/assets/items/newspaper.png',
        transformedImage: '/assets/transformed/paper.png',
        fun_fact: "Recycling one ton of paper (books/notebooks) saves 17 trees, 7,000 gallons of water, and 463 gallons of oil.",
        transformation: "Ink is safely removed to create fresh, recycled office paper or heavy-duty cardboard for industrial shipping boxes.",
        impact: "Paper recycling reduces sulfur dioxide emissions (a cause of acid rain) by nearly 30% compared to virgin paper production.",
        tips: [
            "Remove any plastic wraps or heavy glue from the spine if possible.",
            "Hardcover books should have the cover removed as it's often non-recyclable.",
            "Donate books in good condition to local libraries or charities instead."
        ],
        numericalImpact: { co2: 1200, water: 5000, energy: 400 }
    },
    'paper': {
        image: '/assets/items/cardboard.png',
        transformedImage: '/assets/transformed/paper.png',
        fun_fact: "Paper can be recycled 5 to 7 times before the fibers become too short to be reused.",
        transformation: "Pulped and pressed into new biodegradable egg cartons, cereal cereal boxes, or protective packing material.",
        impact: "Producing recycled paper uses 40% less energy than making it from raw wood pulp.",
        tips: [
            "Do not recycle paper that is wet or stained with food/grease.",
            "Remove any plastic windows from envelopes before recycling.",
            "Shredded paper should be placed in a paper bag to prevent littering."
        ],
        numericalImpact: { co2: 300, water: 1000, energy: 100 }
    },
    'can': {
        image: '/assets/items/can.png',
        transformedImage: '/assets/transformed/metal.png',
        fun_fact: "Aluminum is 'infinitely' recyclable. It can go from the recycling bin to a store shelf as a new can in as little as 60 days.",
        transformation: "Melted in high-heat furnaces to be cast into massive ingots, then rolled into thin sheets for the next generation of soda cans.",
        impact: "Recycling aluminum saves 95% of the energy needed to create it from raw bauxite ore.",
        tips: [
            "Rinse out any remaining residue to keep the recycling stream clean.",
            "Do not crush cans if your local facility uses automated sorting.",
            "Check if the tab can be donated to local charity programs."
        ],
        numericalImpact: { co2: 200, water: 0, energy: 200 }
    },
    'metal': {
        image: '/assets/items/can.png',
        transformedImage: '/assets/transformed/metal.png',
        fun_fact: "Metal is infinitely recyclable. Recycling a single aluminum can saves enough energy to run a TV for three hours!",
        transformation: "Purified and rolled into high-grade sheets used for sustainable car parts or structural beams in green buildings.",
        impact: "Reduces the need for destructive mining and saves up to 95% of the energy used for virgin production.",
        tips: ["Rinse thoroughly", "Do not crush if using automated sorting", "Check for local scrap metal programs."],
        numericalImpact: { co2: 250, water: 0, energy: 250 }
    },
    'tin': {
        image: '/assets/items/tin.png',
        transformedImage: '/assets/transformed/steel_beam.png',
        fun_fact: "Steel is the most recycled material in the world. Every ton of recycled steel saves 2,500 pounds of iron ore.",
        transformation: "Processed by massive electromagnetic sorters and melted into high-strength steel beams for infrastructure projects.",
        impact: "Using recycled steel instead of virgin ore reduces air pollution by 86% and water waste by 76%.",
        tips: [
            "Rinse the can thoroughly and remove the label if possible.",
            "Place the lid inside the can and crimp the top to prevent injury.",
            "Check for 'Recyclable Steel' logos to confirm local acceptance."
        ],
        numericalImpact: { co2: 300, water: 0, energy: 300 }
    },
    'glass': {
        image: '/assets/items/glass.png',
        transformedImage: '/assets/transformed/cullet.png',
        fun_fact: "Glass never wears out—it can be recycled forever. A glass bottle buried today would take 4,000 years to decompose.",
        transformation: "Sanitized and crushed into 'cullet' to be reborn as decorative fiberglass insulation or new high-clarity jars.",
        impact: "Adding recycled glass to the mix reduces the furnace temperature, saving energy and extending the life of the manufacturing plant.",
        tips: [
            "Sort by color (clear, green, brown) if required by your local program.",
            "Remove metal caps and rings, as they are processed separately.",
            "Never include Pyrex, mirrors, or window glass in your recycling bin."
        ],
        numericalImpact: { co2: 100, water: 100, energy: 50 }
    },
    'jar': {
        image: '/assets/items/jar.png',
        transformedImage: '/assets/transformed/cullet.png',
        fun_fact: "Glass jars are often more efficiently recycled than bottles due to their thick, durable nature.",
        transformation: "Cleaned and melted into new food-grade containers or high-durability glass beads for reflective road markings.",
        impact: "Recycling 1,000 tons of glass creates 8 more jobs than simply sending it to a landfill.",
        tips: [
            "Rinse off all food residue, especially sticky sauces or oils.",
            "Remove labels if they are easily peelable, though most facilities can handle them.",
            "Reuse jars at home for bulk food storage or DIY projects."
        ],
        numericalImpact: { co2: 150, water: 150, energy: 80 }
    },
    'banana': {
        image: '/assets/items/banana.png',
        transformedImage: '/assets/transformed/compost.png',
        fun_fact: "Banana peels are 100% biodegradable and exceptionally rich in potassium and phosphorus—perfect for plant growth.",
        transformation: "Diverted to anaerobic digesters to produce clean methane gas for local electricity and liquid bio-fertilizer.",
        impact: "Diverting organics from landfills prevents methane gas production, a greenhouse gas 25x more potent than CO2.",
        tips: [
            "Remove any plastic stickers or produce ties before composting.",
            "Cut into smaller pieces to speed up the decomposition process.",
            "Avoid adding to a 'dry' bin to prevent attracting pests."
        ]
    },
    'apple': {
        image: '/assets/items/apple.png',
        transformedImage: '/assets/transformed/compost.png',
        fun_fact: "Food waste represents nearly 24% of municipal solid waste. An apple core can take just 2 weeks to compost.",
        transformation: "Returned to the earth as premium organic humus, enriching the soil for the next season's apple orchards.",
        impact: "Every kilogram of food waste composted saves the equivalent of 1.5 kg of CO2 emissions.",
        tips: [
            "Keep in a sealed organic waste bin to manage odors.",
            "Apple seeds contain tiny amounts of cyanide—composting safely neutralizes this.",
            "Perfect for vermicomposting (worm bins) as they break down quickly."
        ]
    },
    'laptop': {
        image: '/assets/items/laptop.png',
        transformedImage: '/assets/transformed/minerals.png',
        fun_fact: "Up to 98% of a laptop is recyclable, including the glass screen, plastic casing, and metal internal components.",
        transformation: "Valuable rare-earth elements are extracted from circuit boards to create the batteries and screens of tomorrow's devices.",
        impact: "Prevents hazardous lithium-ion batteries from causing fires in traditional waste trucks and facilities.",
        tips: [
            "Securely wipe your hard drive using data destruction software.",
            "Recycle the power cables and peripherals at the same time.",
            "Consult manufacturer take-back programs for potential credit."
        ],
        numericalImpact: { co2: 15000, water: 20000, energy: 5000 }
    },
    'phone': {
        image: '/assets/items/phone.png',
        transformedImage: '/assets/transformed/minerals.png',
        fun_fact: "One ton of old cell phones contains more gold than many gold mines. They also contain silver, palladium, and copper.",
        transformation: "Dismantled to reclaim precious metals like gold and palladium, ensuring no new destructive mining is needed for future chips.",
        impact: "Proper E-waste recycling prevents lead, mercury, and cadmium from leaching into our groundwater.",
        tips: [
            "Perform a factory reset to protect your personal data.",
            "Remove the SIM card and any external memory cards.",
            "Take to a dedicated E-waste collection point or retailer program."
        ],
        numericalImpact: { co2: 5000, water: 10000, energy: 2000 }
    },
    'plastic bag': {
        image: '/assets/items/plastic_bag.png',
        transformedImage: '/assets/transformed/lumber.png',
        fun_fact: "The average plastic bag is used for 12 minutes but stays in the environment for up to 1,000 years.",
        transformation: "Compressed and heated to form high-durability 'plastic lumber' used for moisture-resistant decks and park benches.",
        impact: "Preventing bag litter saves thousands of marine animals who mistake them for food every year.",
        tips: [
            "Never put these in your curbside bin; they tangle sorting machines.",
            "Return them to grocery store collection bins for proper processing.",
            "Ensure they are completely empty and dry before disposal."
        ],
        numericalImpact: { co2: 30, water: 0, energy: 10 }
    }
};

export const DEFAULT_KNOWLEDGE = {
    'Recycle': {
        fun_fact: "This item is primarily dry waste. If cleaned properly, it has high value in the circular economy.",
        transformation: "It will be reborn as high-quality raw material pellets, forming the building blocks of new sustainable products.",
        impact: "Every item you recycle moves us one step closer to a zero-waste future and preserves natural habitats.",
        tips: [
            "Ensure the item is empty, clean, and dry.",
            "Do not bag your recyclables; leave them loose in the bin.",
            "Check the local rules for specific material acceptance."
        ]
    },
    'Organic': {
        fun_fact: "Organic matter is the 'battery' of the earth, storing nutrients that must be returned to the soil.",
        transformation: "It will undergo transformation into nutrient-dense compost, fueling the growth of new gardens and local ecology.",
        impact: "Organic recycling reduces the need for chemical fertilizers and helps soil retain 20% more moisture.",
        tips: [
            "Exclude any meat, dairy, or oils unless local rules allow them.",
            "Use compostable bags or line your bin with newspaper.",
            "Aim for a mix of 'greens' (food) and 'browns' (leaves/paper)."
        ]
    },
    'Hazardous': {
        fun_fact: "Hazardous waste accounts for only 1% of total waste but causes 90% of toxic contamination issues.",
        transformation: "It will be safely neutralized or distilled into safe chemical components in specialized high-security facilities.",
        impact: "By scanning this, you've prevented toxins from potentially entering the human food chain through soil or water.",
        tips: [
            "Keep items in their original packaging to help identification.",
            "Store safely away from children and pets until disposal.",
            "Never pour hazardous liquids down the drain or onto the ground."
        ]
    },
    'Landfill': {
        fun_fact: "Landfill space is a finite resource. Modern landfills are engineered with complex liners and gas capture systems.",
        transformation: "If correctly managed, it will be safely compacted or processed in energy plants to generate local district heating.",
        impact: "Reducing landfill waste saves cities millions in management costs and prevents land degradation.",
        tips: [
            "Minimize use of single-use items to reduce landfill load.",
            "Bag your trash securely to prevent litter and odors.",
            "Consider if the item can be repaired or donated first."
        ]
    }
};
