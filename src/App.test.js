import { render, screen } from '@testing-library/react';
import App from './App.js';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/Malachi Kakembo /i);
  expect(linkElement).toBeInTheDocument();
});
