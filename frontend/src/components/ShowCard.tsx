import { Card, CardHeader, CardPreview, Button, Body1, Subtitle2 } from '@fluentui/react-components'
import { useNavigate } from 'react-router-dom'
import { ShowCard as ShowCardType } from '../types/api'

interface Props {
  show: ShowCardType
}

export default function ShowCard({ show }: Props) {
  const navigate = useNavigate()
  return (
    <Card style={{ marginBottom: 12 }}>
      <CardHeader
        header={<Subtitle2>{show.showdate}</Subtitle2>}
        description={`${show.venue || 'Venue'}, ${show.city || ''} ${show.state || ''} ${show.country || ''}`}
        action={
          <Button appearance="primary" onClick={() => navigate(`/shows/${show.showdate}`)}>
            View
          </Button>
        }
      />
      <CardPreview>
        <Body1>Show ID: {show.showid ?? 'N/A'}</Body1>
      </CardPreview>
    </Card>
  )
}
