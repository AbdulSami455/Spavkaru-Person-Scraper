import React, { useState } from 'react';
import './App.css';

interface PersonResult {
  name: string;
  phone: string;
  address: string;
  additional_info?: string;
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
      console.log('Sending request with data:', {
        country,
        search_name: searchName,
        city_name: cityName || undefined,
        area_code: areaCode || undefined,
        phone_filter: phoneFilter || undefined,
        address_filter: addressFilter || undefined,
        max_pages: maxPages ? parseInt(maxPages) : undefined,
        results_limit: resultsLimit ? parseInt(resultsLimit) : undefined,
      });

      const response = await fetch('http://localhost:8000/search', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
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
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Search failed');
      }

      const data = await response.json();
      console.log('Received response:', data);

      if (!data.results) {
        throw new Error('Invalid response format from server');
      }

      setResults(data.results);
    } catch (err: any) {
      console.error('Search error:', err);
      setError(err.message || 'An error occurred during the search');
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
          <input 
            value={searchName} 
            onChange={e => setSearchName(e.target.value)} 
            required 
            placeholder="Enter full name"
          />
        </label>
        <label>
          City Name:
          <input 
            value={cityName} 
            onChange={e => setCityName(e.target.value)} 
            placeholder="Optional"
          />
        </label>
        <label>
          Area Code:
          <input 
            value={areaCode} 
            onChange={e => setAreaCode(e.target.value)} 
            placeholder="Optional"
          />
        </label>
        <label>
          Phone Filter:
          <input 
            value={phoneFilter} 
            onChange={e => setPhoneFilter(e.target.value)} 
            placeholder="Optional"
          />
        </label>
        <label>
          Address Filter:
          <input 
            value={addressFilter} 
            onChange={e => setAddressFilter(e.target.value)} 
            placeholder="Optional"
          />
        </label>
        <label>
          Max Pages:
          <input 
            type="number" 
            min="1" 
            value={maxPages} 
            onChange={e => setMaxPages(e.target.value)} 
            placeholder="Optional"
          />
        </label>
        <label>
          Results Limit:
          <input 
            type="number" 
            min="1" 
            value={resultsLimit} 
            onChange={e => setResultsLimit(e.target.value)} 
            placeholder="Optional"
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>
      
      {loading && <p className="loading">Searching...</p>}
      {error && <p className="error">{error}</p>}
      
      {results.length > 0 ? (
        <div className="results-container">
          <h2>Search Results ({results.length})</h2>
          <table className="results-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Phone</th>
                <th>Address</th>
                <th>Additional Info</th>
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={i}>
                  <td>{r.name}</td>
                  <td>{r.phone}</td>
                  <td>{r.address}</td>
                  <td>{r.additional_info}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : !loading && !error && (
        <p className="no-results">No results found. Try adjusting your search criteria.</p>
      )}
    </div>
  );
}

export default App;
