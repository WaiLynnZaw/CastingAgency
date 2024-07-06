import { useAuth0 } from '@auth0/auth0-react';
import { useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';

const usePermissions = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [permissions, setPermissions] = useState([]);

  useEffect(() => {
    const fetchPermissions = async () => {
      try {
        const token = await getAccessTokenSilently();
        const decodedToken = jwtDecode(token);

        if (decodedToken && decodedToken.permissions) {
          setPermissions(decodedToken.permissions);
        }
      } catch (error) {
        console.error('Error fetching permissions:', error);
      }
    };

    fetchPermissions();
  }, [getAccessTokenSilently]);

  const hasPermission = (permission) => {
    return permissions.includes(permission);
  };

  return { hasPermission };
};

export default usePermissions;

