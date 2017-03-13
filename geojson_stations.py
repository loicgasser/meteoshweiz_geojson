# -*- coding: utf-8 -*-
import os
import sys
import json
import geojson
import datetime


def create_geojson_feature(id, x, y, z, properties):
    return {
        'id': id,
        'geometry': {
            'type': 'Point',
            'coordinates': [x, y, z]
        },
        'properties': properties,
        'type': 'Feature'
    }


def create_geosjon_file(features):
    date = datetime.datetime.now()
    featuresCollection = geojson.FeatureCollection(features)
    featuresCollection['mapname'] = 'ch.swissmetnet.stations'
    featuresCollection['timestamp'] = date.strftime('%d.%m.%Y %H:%M')
    with open('data/stations.json', 'wb') as f:
        f.write(
            json.dumps(featuresCollection)
        )


def create_row(name, value, url=None):
    if url is None:
        return '<tr><td><strong>%s</strong></td><td>%s</td></tr>' % (name, value)
    url = 'http://www.meteosuisse.admin.ch' + url
    return '<tr><td><strong>%s</strong></td><td><a href=\'%s\' target=\'_blank\'>%s</a></td></tr>' % (name, url, value)


def to_bool(value):
    return True if value == 1 else False


def create_description(id, properties):
    attr_to_labels = {
        u'sun_duration': u'Durée de l\'ensoleillement',
        u'temperature_2m': u'Température de l\'air',
        u'airpressure': u'Pression de l\'air',
        u'rel_humidity': u'Humidité relative',
        u'wind': u'Vitesse du vent',
        u'radiation_global': u'Rayonnement global',
        u'precipitation': u'Précipitations'
    }

    # One template per language
    tmp = '<table>'
    tmp += create_row(u'Altitude', properties['height'])
    tmp += create_row(u'Abréviation', id)
    tmp += create_row(u'Officielle depuis', properties['date_officialized'])
    tmp += '<tr><td><strong>Programme de mesures</strong></td>'
    tmp += '<td>'
    for measure_pt in attr_to_labels.keys():
        if properties[measure_pt]:
            tmp += '%s<br>' % attr_to_labels[measure_pt]
    tmp += '</td></tr>'
    if properties['remarks']:
        tmp += create_row(u'Particularitées', properties['remarks'])
    tmp += create_row('Fiche technique de la station de mesure', properties['data_name'], url=properties['data_url'])
    tmp += '</table>'
    return tmp


def main():
    if len(sys.argv) != 2:
        print('Please provide a json file')
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print('File %s does not exist' % file_path)
        sys.exit(1)

    with open(file_path, 'r') as f:
        content = json.load(f)

    features = []
    for feat in content['stations']:
        id = feat.get('code')
        x = float(feat['coord_x'])
        y = float(feat['coord_y'])
        z = float(feat['height'])
        img = feat.get('image')
        data = feat.get('datasheet')
        sensors = feat.get('sensors')
        properties = {}
        properties['name'] = feat.get('name')
        properties['date_officialized'] = feat.get('date_officialized')
        properties['height'] = feat.get('height')
        properties['remarks'] = feat.get('remarks')
        properties['image_url'] = img.get('url')
        properties['image_caption'] = img.get('caption')
        properties['data_url'] = data.get('url')
        properties['data_size'] = data.get('size')
        properties['data_name'] = data.get('name')
        properties['data_lang'] = data.get('language')
        # Denotes the sensors
        properties['sun_duration'] = to_bool(sensors.get('sun_duration'))
        properties['temperature_2m'] = to_bool(sensors.get('temperature_2m'))
        properties['airpressure'] = to_bool(sensors.get('airpressure'))
        properties['rel_humidity'] = to_bool(sensors.get('rel_humidity'))
        properties['radiation_global'] = to_bool(sensors.get('radiation_global'))
        properties['precipitation'] = to_bool(sensors.get('precipitation'))
        properties['wind'] = to_bool(sensors.get('wind'))
        properties['description'] = create_description(id, properties)

        features.append(create_geojson_feature(id, x, y, z, properties))

    create_geosjon_file(features)


if __name__ == '__main__':
    main()
