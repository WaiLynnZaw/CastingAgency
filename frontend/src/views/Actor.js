import React, { useEffect, useState } from 'react';
import Swal from 'sweetalert2';
import { useAuth0, withAuthenticationRequired } from '@auth0/auth0-react';
import { getConfig } from '../config';
import { useHistory } from "react-router-dom";
import usePermissions from '../utils/permissions';
import Loading from "../components/Loading";

export const ActorComponent = () => {
  const { apiOrigin = 'https://casting-agency-api-v0sn.onrender.com' } = getConfig();
  const { getAccessTokenSilently } = useAuth0();
  const { hasPermission } = usePermissions();
  const [actors, setActors] = useState([]);
  const history = useHistory();

  useEffect(() => {
    const fetchActors = async () => {
      try {
        const token = await getAccessTokenSilently();
        const response = await fetch(`${apiOrigin}/actors`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        setActors(data.actors);
      } catch (error) {
        console.error('Error fetching actors:', error);
      }
    };

    fetchActors();
  }, [apiOrigin, getAccessTokenSilently, hasPermission]);

  const handleDeleteActor = async (id) => {
    if (!hasPermission('delete:actor')) {
      return Swal.fire({
        icon: 'error',
        title: 'Error!',
        text: 'You do not have permission to delete a actor.',
        showConfirmButton: true,
      });
    }
    const result = await Swal.fire({
      icon: 'warning',
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      showCancelButton: true,
      confirmButtonText: 'Yes, delete it!',
      cancelButtonText: 'No, cancel!',
    });

    if (result.isConfirmed) {
      try {
        const token = await getAccessTokenSilently();
        await fetch(`${apiOrigin}/actors/${id}`, {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        Swal.fire(
          'Deleted!',
          'The actor has been deleted.',
          'success'
        );
        setActors(actors.filter((m) => m.id !== id));
      } catch (error) {
        Swal.fire({
          icon: 'error',
          title: 'Error!',
          text: 'There was an error deleting the actor.',
          showConfirmButton: true,
        });
      }
    }
  };

  return (
    <div className="container">
      <h1>Actors</h1>
      <div style={{ marginBottom: '18px' }}>
        {hasPermission('post:actors') && (
          <button onClick={() => history.push('/add-actor')}>Add Actor</button>
        )}
      </div>
      <div className="contain-table">
        <table className="striped-table">
          <thead>
            <tr>
              <th>No.</th>
              <th>Name</th>
              <th>Age</th>
              <th>Gender</th>
              <th colSpan={2} className="text-center">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            {actors.length > 0 ? (
              actors.map((actor, i) => (
                <tr key={actor.id}>
                  <td>{i + 1}</td>
                  <td>{actor.name}</td>
                  <td>{actor.age}</td>
                  <td>{actor.gender}</td>
                  <td className="text-right">
                    {hasPermission('patch:actor') && (
                      <button
                        onClick={() => history.push(`/edit-actor/${actor.id}`)}
                        className="button muted-button"
                      >
                        Edit
                      </button>
                    )}
                  </td>
                  <td className="text-left">
                    {hasPermission('delete:actor') && (
                      <button
                        onClick={() => handleDeleteActor(actor.id)}
                        className="button muted-button"
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                  <td colSpan={7} className="text-center">No Actor found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default withAuthenticationRequired(ActorComponent, {
  onRedirecting: () => <Loading />,
});
