const chai = require('chai');
const chaiHttp = require('chai-http');
const app = require('../app'); // Assuming your Express app is exported from app.js
const expect = chai.expect;

chai.use(chaiHttp);

describe('Items API', () => {
    describe('GET /items', () => {
        it('should return all items', async () => {
            const res = await chai.request(app).get('/items');
            expect(res).to.have.status(200);
            expect(res.body).to.be.an('array');
        });

        it('should return status 404 if no items are found', async () => {
            const res = await chai.request(app).get('/items');
            expect(res).to.have.status(404);
            expect(res.body).to.have.property('error');
        });
    });
});
