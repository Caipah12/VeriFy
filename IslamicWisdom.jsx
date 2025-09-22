import React, { useState, useEffect } from 'react';

const islamicWisdom = [
  {
    type: 'Quran',
    text: "O you who have believed, if there comes to you a disobedient one with information, investigate it, lest you harm a people out of ignorance and become, over what you have done, regretful.",
    source: "Surah Al-Hujurat: 6"
  },
  {
    type: 'Quran',
    text: "And do not pursue that of which you have no knowledge. Indeed, the hearing, the sight, and the heart—about all those [one] will be questioned.",
    source: "Surah Al-Isra': 36"
  },
  {
    type: 'Quran',
    text: "And say, 'The truth has come, and falsehood has departed. Indeed, falsehood is [by nature] ever bound to depart.'",
    source: "Surah Al-Isra': 81"
  },
  {
    type: 'Hadith',
    text: "It is enough for a person to be considered a liar that he narrates everything he hears.",
    source: "Sahih Muslim, No. 5"
  },
  {
    type: 'Hadith',
    text: "Whoever believes in Allah and the Last Day should speak good or remain silent.",
    source: "Sahih Bukhari, No. 6018; Sahih Muslim, No. 47"
  },
  {
    type: 'Hadith',
    text: "He is not one of us who spreads mischief and evil among people.",
    source: "Musnad Ahmad, No. 28676"
  }
];

export default function IslamicWisdom() {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % islamicWisdom.length);
    }, 60000); // Change every minute

    return () => clearInterval(interval);
  }, []);

  const currentWisdom = islamicWisdom[currentIndex];
  const bgColor = currentWisdom.type === 'Quran' ? 'bg-purple-50' : 'bg-blue-50';
  const textColor = currentWisdom.type === 'Quran' ? 'text-purple-800' : 'text-blue-800';
  const sourceColor = currentWisdom.type === 'Quran' ? 'text-purple-600' : 'text-blue-600';

  return (
    <div className="glass-card p-6 mb-6">
      <h3 className="text-xl font-bold text-purple-900 mb-4">Verify with iNaQ</h3>
      <div className={`${bgColor} rounded-lg p-4`}>
        <h4 className="font-semibold text-purple-900 mb-2">
          {currentWisdom.type === 'Quran' ? 'Verse from the Quran' : 'Hadith of Prophet Muhammad (PBUH)'}
        </h4>
        <p className={`italic ${textColor} mb-2`}>{currentWisdom.text}</p>
        <p className={`text-sm ${sourceColor}`}>- {currentWisdom.source}</p>
      </div>
    </div>
  );
}