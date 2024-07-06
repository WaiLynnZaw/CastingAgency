import React, { useState } from 'react';
import Swal from 'sweetalert2';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';
import { getConfig } from '../config';
import { useHistory } from 'react-router-dom';
import usePermissions from '../utils/permissions';
import Loading from "../components/Loading";

export const AddActorForm = () => {
  const { apiOrigin = "https://casting-agency-api-v0sn.onrender.com" } = getConfig();
  const { getAccessTokenSilently } = useAuth0();
  const { hasPermission } = usePermissions();
  const history = useHistory();
  
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');

  const handleAdd = async (e) => {
    e.preventDefault();
    
    if (!hasPermission('post:actors')) {
      return Swal.fire({
        icon: 'error',
        title: 'Unauthorized!',
        text: 'You do not have permission to add a new actor.',
        showConfirmButton: true,
      });
    }

    if (!name || !age || !gender) {
      return Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'All fields are required.',
        showConfirmButton: true,
      });
    }

    try {
      const token = await getAccessTokenSilently();
      await fetch(`${apiOrigin}/actors`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, age, gender }),
      });

      Swal.fire({
        icon: 'success',
        title: 'Added!',
        text: `${name} has been added.`,
        showConfirmButton: false,
        timer: 1500,
      });

      history.push('/actors');
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'There was an error adding the actor.',
        showConfirmButton: true,
      });
    }
  };

  return (
    <div className="small-container">
      <form onSubmit={handleAdd}>
        <h1>Add Actor</h1>
        <label htmlFor="name">Name</label>
        <input
          id="name"
          type="text"
          name="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <label htmlFor="age">Age</label>
        <input
          id="age"
          type="number"
          name="age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />
        <label htmlFor="gender">Gender</label>
        <select
          id="gender"
          name="gender"
          value={gender}
          onChange={(e) => setGender(e.target.value)}
        >
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
        <div style={{ marginTop: '30px' }}>
          <input type="submit" value="Add" />
          <input
            style={{ marginLeft: '12px' }}
            className="muted-button"
            type="button"
            value="Cancel"
            onClick={() => history.push('/actors')}
          />
        </div>
      </form>
    </div>
  );
};

export default withAuthenticationRequired(AddActorForm, {
  onRedirecting: () => <Loading />,
});