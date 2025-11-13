General Rules

Ensure the code follows the project’s coding standards and naming conventions.
Verify that no sensitive information (API keys, credentials) is committed.
Confirm that all new features or fixes are relevant to the Movie Website functionality.


🎬 Movie Website Specific Checks


UI/UX Consistency

Pages should maintain the existing design style and layout.
Navigation between movie listings, details, and search should work seamlessly.



Movie Data Handling

Ensure movie details (title, genre, rating, description) are displayed correctly.
Validate that API calls for fetching movies are optimized and error-handled.



Search & Filter Functionality

Check that search results update dynamically and filters work as expected.
No broken links or empty states without proper messages.



Performance

Avoid unnecessary API calls or heavy operations on the client side.
Confirm lazy loading or pagination for large movie lists.




🧪 Testing Requirements

Unit tests should cover new components or logic.
Integration tests for API calls and UI flows must pass.
No failing tests in the pipeline.


🔒 Security

Validate input fields to prevent XSS or injection attacks.
Ensure API keys or tokens are not exposed in the code.


📄 Documentation

Update README or relevant docs if new features are added.
Include comments for complex logic or API integration.


✅ PR Checklist
Before approving, confirm:

Code is clean and readable.
No console logs or debug statements.
All tests pass successfully.
No merge conflicts.
Follows accessibility guidelines (alt text for images, proper labels).

