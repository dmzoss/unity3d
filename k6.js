import http from 'k6/http';
import { sleep } from 'k6';
export const options = {
  vus: 15,
  duration: '300s',
};

export default function () {
  http.get('http://localhost:8080/getAllUserBuys');
  sleep(1);
}
