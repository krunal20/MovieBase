import React, { useState } from 'react';
import axios from 'axios';
import './Search.css';
import defaultImage from '../assets/images/default.jpg';

function Search() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filtersVisible, setFiltersVisible] = useState(false);
  const [filters, setFilters] = useState({
    Genre: '',
    Released_Year: '',
    IMDB_Rating: '',
    certificate: '',
  });
  const [sortBy, setSortBy] = useState('rating');

  // Updated image mapping with local assets
  const getImageUrl = (Genre) => {
    try {
      return require(`../assets/images/${Genre.toLowerCase()}.jpg`);
    } catch (e) {
      return defaultImage;
    }
  };

  const handleSearch = async (filtersOverride = filters) => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setFiltersVisible(true); // Show filters after the first search

    try {
      const response = await axios.get('/api/search', {
        params: {
          q: query,
          Genre: filtersOverride.Genre || '',
          Released_Year: filtersOverride.Released_Year || '',
          IMDB_Rating: filtersOverride.IMDB_Rating || '',
          certificate: filtersOverride.certificate || '',
          sort: sortBy || 'rating'
        }
      });

      const resultsWithImages = response.data.map(result => ({
        title: result.Series_Title,
        genre: result.Genre,
        year: result.Released_Year,
        rating: result.IMDB_Rating,
        certificate: result.Certificate,
        image: result.Poster_Link || defaultImage
      }));
      
      setResults(resultsWithImages);
    } catch (err) {
      setError('Failed to fetch results. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (filterKey, value) => {
    const updatedFilters = { ...filters, [filterKey]: value };
    setFilters(updatedFilters);
    handleSearch(updatedFilters);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="search-container">
      <h1>Discover the best movies of all time!</h1>

      <div className="search-box">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="What are you looking for?"
          aria-label="Search movies or shows"
        />
        <button 
          onClick={() => handleSearch()} 
          disabled={!query.trim()}
          aria-label="Search button"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      {filtersVisible && (
        <div className="filters">
          <select value={filters.Genre} onChange={(e) => handleFilterChange('Genre', e.target.value)}>
            <option value="">All Genres</option>
            <option value="action">Action</option>
            <option value="comedy">Comedy</option>
            <option value="drama">Drama</option>
            <option value="horror">Horror</option>
            <option value="romance">Romance</option>
          </select>

          <input
            type="text"
            placeholder="Year"
            value={filters.Released_Year}
            onChange={(e) => handleFilterChange('Released_Year', e.target.value)}
          />

          <input
            type="number"
            placeholder="Minimum Rating"
            value={filters.IMDB_Rating}
            onChange={(e) => handleFilterChange('IMDB_Rating', e.target.value)}
          />

          <select value={filters.certificate} onChange={(e) => handleFilterChange('certificate', e.target.value)}>
            <option value="">All Certificates</option>
            <option value="PG">PG</option>
            <option value="PG-13">PG-13</option>
            <option value="R">R</option>
            <option value="G">G</option>
          </select>
        </div>
      )}

      {error && <div className="error" role="alert">{error}</div>}

      {results.length > 0 ? (
        <div className="results">
          {results.map((result, index) => (
            <div key={index} className="result-card">
              <img 
                src={result.image} 
                alt={result.title || 'Result'}
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = defaultImage;
                }}
              />
              <h3>{result.title}</h3>
              <p><strong>Genre:</strong> {result.genre}</p>
              <p><strong>Year:</strong> {result.year}</p>
              <p><strong>Rating:</strong> {result.rating}/10</p>
              <p><strong>Certificate:</strong> {result.certificate}</p>
            </div>
          ))}
        </div>
      ) : (
        <p className="no-results">{!loading && query && 'No results found'}</p>
      )}
    </div>
  );
}

export default Search;
