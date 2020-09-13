//import 'bootstrap/dist/css/bootstrap.css';
import { ReactWidget } from '@jupyterlab/apputils';
import React, { useState } from 'react';
import NavBar from './NavBar';

/**
 * React component for a counter.
 *
 * @returns The React component
 */
const CounterComponent = (): JSX.Element => {
  const [counter, setCounter] = useState(0);

  return (
    <div>
      <p>You clicked {counter} times!</p>
      <button
        onClick={(): void => {
          setCounter(counter + 1);
        }}
      >
        Increment
      </button>
    </div>
  );
};

/**
 * A Counter Lumino Widget that wraps a CounterComponent.
 */
export class CondaStoreWidget extends ReactWidget {
  /**
   * Constructs a new CounterWidget.
   */
  constructor() {
    super();
    this.addClass('jp-ReactWidget');
  }

  render(): JSX.Element {
	  return(
		  <div>
			  <NavBar/>
			  <CounterComponent />
		  </div>
	  );
  }
}
