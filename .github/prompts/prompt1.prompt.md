---
mode: agent
---
---
mode: agent
---

# Search Module Prompt

You are an AI assistant helping to implement a search functionality for a movie website. Generate code and implementations that follow these requirements:

## Context
This is for a movie website where users can search for movies by title, genre, or year. The search should be fast, user-friendly, and return relevant results.

## Task Requirements
When asked to implement search functionality, you should:

1. **Search Implementation:**
    - Create search endpoints that accept query parameters for title, genre, and year
    - Implement efficient database queries with proper indexing
    - Support partial matching and case-insensitive searches
    - Include pagination for search results

2. **API Design:**
    - RESTful endpoints following pattern: `/api/movies/search?q={query}&filter={type}&page={number}`
    - Proper HTTP status codes and error responses
    - Input validation and sanitization
    - Rate limiting for search requests

3. **Frontend Components:**
    - Search input field with autocomplete suggestions
    - Filter options for genre and year range
    - Results display with movie cards showing title, year, genre, synopsis
    - Loading states and error handling
    - Mobile-responsive design

4. **Performance Optimization:**
    - Implement search result caching
    - Debounced search input to reduce API calls
    - Lazy loading for search results
    - Efficient database indexing strategies

5. **Security Considerations:**
    - SQL injection prevention
    - Input sanitization and validation
    - Authentication checks for protected searches
    - Proper error messages without data exposure

## Output Format
- Provide complete, working code examples
- Include proper error handling and validation
- Add comments explaining key functionality
- Follow the project's coding standards
- Include unit tests where appropriate

## Example Usage
