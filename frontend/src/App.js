import React, { useState } from 'react';

function App() {
  const [sumInsured, setSumInsured] = useState(300000);
  const [cityTier, setCityTier] = useState('tier-1');
  const [tenure, setTenure] = useState('1yr');
  const [members, setMembers] = useState('46, 35, 10');
  const [premium, setPremium] = useState(0);

  const calculatePremium = async () => {
    const member_ages = members.split(',').map(member => Number(member.trim()))
    const response = await fetch('http://localhost:8080/calculate_premium', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sum_insured: sumInsured,
        city_tier: cityTier,
        tenure: tenure,
        member_ages: member_ages,
      }),
    });
    const data = await response.json();
    setPremium(data.premium);
  };

  return (
    <div style={{fontSize: '20px', padding: '5% 30%', textAlign: 'center'}}>
      <h1>Health Insurance Premium Calculator</h1>
      <form style={{display: 'flex', flexDirection: 'column', gap: '20px', textAlign: 'left'}}>
        {/* Add input fields for sum insured, city tier, tenure, and member ages */}
        <label for="sum_insured">Sum Insured</label>
        <input id="sum_insured" type="number" required value={sumInsured} onChange={(e) => setSumInsured(Number(e.target.value))}/>

        <label for="city_tier">City Tier</label>
        <input id="" type="text" required value={cityTier} onChange={(e) => setCityTier(e.target.value)}/>

        <label for="tenure">Tenure</label>
        <input id="tenure" type="text" required value={tenure} onChange={(e) => setTenure(e.target.value)}/>

        <label for="members">Members (comma separated)</label>
        <input id="members" type="text" required value={members} onChange={(e) => setMembers(e.target.value)}/>

        {/* Calculate Premium */}
        <button type='button' style={{padding: '20px'}} onClick={calculatePremium}>Calculate Premium</button>
      </form>
      {/* Display the calculated premium */}
      <h2 style={{margin: '30px'}}>{premium}</h2>
    </div>
  );
}

export default App;
