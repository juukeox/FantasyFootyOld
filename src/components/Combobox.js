import React from 'react';

function ComboBox({ options, id, onChange }) {
  const comboBoxStyles = {
    display: 'block',
    marginBottom: '25px',
    width: '300px',
    fontWeight: 'bold',        // Apply bold style
    fontFamily: 'Arial',       // Change font to Arial
    fontSize: '16px',          // Change font size to 16px
    // Add any other text-related styles here
  };

  const handleSelectChange = (event) => {
    const selectedValue = event.target.value;
    const selectedOption = options.find((option) => option.value === selectedValue);
    onChange(selectedOption);
  };

  return (
    <select style={comboBoxStyles} id={id} onChange={handleSelectChange}>
      {options.map((option, index) => (
        <option key={`${id}_${index}`} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
}

export default ComboBox;