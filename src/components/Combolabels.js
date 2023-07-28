// combolabels.js
import React from 'react';

const labelData = [
  { id: 'team', text: 'Which team do you support?:' },
  { id: 'teamSupport', text: 'How much do you want your team represented?:' },
  { id: 'form', text: 'How important is recent form?:' },
  { id: 'efficiency', text: 'Efficiency - How important is points per game?:' },
  { id: 'value', text: 'Looking for good value? How important is points per million? :' },
  { id: 'differential', text: 'Want to get the edge? How important are rarely-owned players?:' },
  { id: 'position', text: 'Position:' },
  { id: 'budget', text: 'Budget:' },
];

function Labels({ id }) {
  const labelStyle = {
    fontWeight: 'bold',
    fontSize: '21px',
    marginBottom: '20px',
    textDecoration: 'underline',  // Apply underline style
    //textDecorationColor: 'red', // Change underline color to red
   // textTransform: 'uppercase',  // Convert the text to uppercase for a title-like effect
 };

  const labelItem = labelData.find(item => item.id === id);

  return (
    <div style={{ marginBottom: '10px' }}>
      {labelItem && (
        <label htmlFor={id} style={labelStyle}>
          {labelItem.text}
        </label>
      )}
    </div>
  );
}

export default Labels;