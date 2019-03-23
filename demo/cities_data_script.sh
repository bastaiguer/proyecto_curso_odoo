#!/bin/bash/

i=0;
echo '
<odoo>
  <data>'
arrayNombres=("Barcelona" "Xátiva")
arrayLugares=("Catalunya" "Comunidad Valenciana" )
arrayDescripciones=("Lugar perfecto para el Ocio, con gran actividad" "Una ciudad preciosa con una buena gastronomía" "Ciudad para perderte entre sus monumentos" "Zonas rurales cerquísimas, rodeado de naturaleza")
while [ $i -lt 2 ] ; do
	desc=$((( RANDOM % 4 ) + 0))
	echo '
    <record id="city'$i'" model="hoteltrivago.cities">
      <field name="name">'${arrayNombres[$i]}'</field>
      <field name="description">'${arrayDescripciones[$desc]}'</field>
      <field name="location">'${arrayLugares[$i]}'</field>
      <field name="country" ref="base.es"/>
    </record>
'

i=$(($i+1));
done
echo '
  </data>
</odoo>'
