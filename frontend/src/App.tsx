import React, { useState } from 'react';
import './App.css';

interface PersonResult {
  name: string;
  phone: string;
  address: string;
}

const countries = [
  { value: 'belarus', label: 'Belarus' },
  { value: 'kazakhstan', label: 'Kazakhstan' },
  { value: 'latvia', label: 'Latvia' },
  { value: 'moldova', label: 'Moldova' },
  { value: 'russia', label: 'Russia' },
  { value: 'ukraine', label: 'Ukraine' },
];

function App() {
  const [country, setCountry] = useState('belarus');
  const [searchName, setSearchName] = useState('');
  const [cityName, setCityName] = useState('');
  const [areaCode, setAreaCode] = useState('');
  const [phoneFilter, setPhoneFilter] = useState('');
  const [addressFilter, setAddressFilter] = useState('');
  const [maxPages, setMaxPages] = useState('');
  const [resultsLimit, setResultsLimit] = useState('');
  const [results, setResults] = useState<PersonResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResults([]);
    try {
      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          country,
          search_name: searchName,
          city_name: cityName || undefined,
          area_code: areaCode || undefined,
          phone_filter: phoneFilter || undefined,
          address_filter: addressFilter || undefined,
          max_pages: maxPages ? parseInt(maxPages) : undefined,
          results_limit: resultsLimit ? parseInt(resultsLimit) : undefined,
        }),
      });
      if (!response.ok) {
        throw new Error('Search failed');
      }
      const data = await response.json();
      setResults(data.results || []);
    } catch (err: any) {
      setError(err.message || 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Spavkaru Person Scraper</h1>
      <form onSubmit={handleSubmit} className="search-form">
        <label>
          Country:
          <select value={country} onChange={e => setCountry(e.target.value)}>
            {countries.map(c => (
              <option key={c.value} value={c.value}>{c.label}</option>
            ))}
          </select>
        </label>
        <label>
          Name:
          <input value={searchName} onChange={e => setSearchName(e.target.value)} required />
        </label>
        <label>
          City Name:
          <input value={cityName} onChange={e => setCityName(e.target.value)} />
        </label>
        <label>
          Area Code:
          <input value={areaCode} onChange={e => setAreaCode(e.target.value)} />
        </label>
        <label>
          Phone Filter:
          <input value={phoneFilter} onChange={e => setPhoneFilter(e.target.value)} />
        </label>
        <label>
          Address Filter:
          <input value={addressFilter} onChange={e => setAddressFilter(e.target.value)} />
        </label>
        <label>
          Max Pages:
          <input type="number" min="1" value={maxPages} onChange={e => setMaxPages(e.target.value)} />
        </label>
        <label>
          Results Limit:
          <input type="number" min="1" value={resultsLimit} onChange={e => setResultsLimit(e.target.value)} />
        </label>
        <button type="submit" disabled={loading}>Search</button>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p style={{color: 'red'}}>{error}</p>}
      {results.length > 0 && (
        <table className="results-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th>Address</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r, i) => (
              <tr key={i}>
                <td>{r.name}</td>
                <td>{r.phone}</td>
                <td>{r.address}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default App;
