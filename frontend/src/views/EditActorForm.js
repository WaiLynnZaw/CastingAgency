import React, { useState, useEffect } from 'react';
import Swal from 'sweetalert2';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';
import { getConfig } from '../config';
import { useHistory, useParams } from 'react-router-dom';
import usePermissions from '../utils/permissions';
import Loading from "../components/Loading";
import authConfig from "../auth_config.json"
export const EditActorForm = () => {
  const { apiOrigin = authConfig.baseUrl } = getConfig();
  const { getAccessTokenSilently } = useAuth0();
  const { hasPermission } = usePermissions();
  const history = useHistory();
  const { id } = useParams();
  
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');

  useEffect(() => {
    const fetchActor = async () => {
      try {
        const token = await getAccessTokenSilently();
        const response = await fetch(`${apiOrigin}/actors/${id}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await response.json();
        setName(data.actor.name);
        setAge(data.actor.age);
        setGender(data.actor.gender);
      } catch (error) {
        console.error('Error fetching actor:', error);
      }
    };

    fetchActor();
  }, [id, apiOrigin, getAccessTokenSilently]);

  const handleEdit = async (e) => {
    e.preventDefault();

    if (!hasPermission('patch:actor')) {
      return Swal.fire({
        icon: 'error',
        title: 'Unauthorized!',
        text: 'You do not have permission to edit this actor.',
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
      await fetch(`${apiOrigin}/actors/${id}`, {
        method: "PATCH",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, age, gender }),
      });

      Swal.fire({
        icon: 'success',
        title: 'Updated!',
        text: `${name} has been updated.`,
        showConfirmButton: false,
        timer: 1500,
      });

      history.push('/actors');
    } catch (error) {
      Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'There was an error updating the actor.',
        showConfirmButton: true,
      });
    }
  };

  return (
    <div className="small-container">
      <form onSubmit={handleEdit}>
        <h1>Edit Actor</h1>
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
          <input type="submit" value="Update" />
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

export default withAuthenticationRequired(EditActorForm, {
  onRedirecting: () => <Loading />,
});