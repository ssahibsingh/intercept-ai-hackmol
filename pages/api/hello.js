export default function handler(req, res) {
  res.status(200).json({ status: 'active', message: 'Intercept AI' })
}
